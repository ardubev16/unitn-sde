#!/usr/bin/env python3

import argparse
import logging
import threading
from pathlib import Path
from uuid import uuid4

from kafka import KafkaConsumer, KafkaProducer

from src import cpu, memory, webcam

logging.basicConfig(level=logging.INFO)
TOPICS = ["cpu", "memory", "webcam", "cpu_mem"]
REMOTE_SERVER = "172.31.199.2:9094"
LOCAL_SERVER = "localhost:9094"


def consume_cpu_mem(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["cpu", "memory"])
    for msg in consumer:
        print(msg)


def get_user_id() -> str:
    user_file_path = Path("/tmp/kafka-lab-user-id")  # NOQA: S108
    if user_file_path.exists():
        with user_file_path.open() as f:
            return f.read()

    new_user_id = str(uuid4())
    with user_file_path.open("w") as f:
        f.write(new_user_id)

    return new_user_id


def producer(bootstrap_server: str, topic: str, user_id: str) -> None:
    producer = KafkaProducer(bootstrap_servers=bootstrap_server)
    match topic:
        case "cpu":
            cpu.produce(producer, user_id)
        case "memory":
            memory.ex1_produce(producer, user_id)
        case "webcam":
            webcam.produce(producer, "https://hd-auth.skylinewebcams.com/live.m3u8?a=iomkvtaeogle92ctjjr9c8r770")
        case "cpu_mem":
            t_cpu = threading.Thread(target=cpu.produce, args=(producer, user_id))
            t_memory = threading.Thread(target=memory.ex1_produce, args=(producer, user_id))

            t_cpu.start()
            t_memory.start()
            t_cpu.join()
            t_memory.join()
        case _:
            raise SystemExit(1)


def consumer(bootstrap_server: str, topic: str, group_id: str) -> None:
    consumer = KafkaConsumer(group_id=group_id, bootstrap_servers=bootstrap_server)
    match topic:
        case "cpu":
            cpu.consume(consumer)
        case "memory":
            memory.consume(consumer)
        case "webcam":
            webcam.consume(consumer)
        case "cpu_mem":
            consume_cpu_mem(consumer)
        case _:
            raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--local", action="store_true", help="Use local Kafka server")
    parser.add_argument("-t", "--topic", choices=TOPICS, required=True, help="Kafka topic")
    subparsers = parser.add_subparsers(required=True, dest="subparser")
    producer_parser = subparsers.add_parser("producer")
    consumer_parser = subparsers.add_parser("consumer")
    consumer_parser.add_argument("-g", "--groupid", default=None, help="Kafka group id")
    args = parser.parse_args()

    bootstrap_server = REMOTE_SERVER
    if args.local:
        bootstrap_server = LOCAL_SERVER

    user_id = get_user_id()
    match args.subparser:
        case "producer":
            producer(bootstrap_server, args.topic, user_id)
        case "consumer":
            consumer(bootstrap_server, args.topic, args.groupid)
        case _:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
