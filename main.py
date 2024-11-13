#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path
from uuid import uuid4

from kafka import KafkaConsumer, KafkaProducer

from src import cpu, jpeg

logging.basicConfig(level=logging.INFO)
TOPICS = ["cpu", "jpeg"]
REMOTE_SERVER = "172.31.199.2:9094"
LOCAL_SERVER = "localhost:9094"


def get_user_id() -> str:
    user_file_path = Path("/tmp/kafka-lab-user-id")  # NOQA: S108
    if user_file_path.exists():
        with user_file_path.open() as f:
            return f.read()

    new_user_id = str(uuid4())
    with user_file_path.open("w") as f:
        f.write(new_user_id)

    return new_user_id


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
            producer = KafkaProducer(bootstrap_servers=bootstrap_server)
            if args.topic == "cpu":
                cpu.produce(producer, user_id)
            elif args.topic == "jpeg":
                jpeg.produce(producer, "https://hd-auth.skylinewebcams.com/live.m3u8?a=iomkvtaeogle92ctjjr9c8r770")

        case "consumer":
            consumer = KafkaConsumer(group_id=args.groupid, bootstrap_servers=bootstrap_server)
            if args.topic == "cpu":
                cpu.consume(consumer)
            elif args.topic == "jpeg":
                jpeg.consume(consumer)


if __name__ == "__main__":
    main()
