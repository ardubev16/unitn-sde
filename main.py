#!/usr/bin/env python3

import argparse
import json
import logging
import time
from typing import NoReturn

import psutil
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(level=logging.INFO)
BOOTSTRAP_SERVER = "172.31.199.2:9094"
# BOOTSTRAP_SERVER = "localhost:9094"


def consume_and_print(group_id: str) -> None:
    consumer = KafkaConsumer(
        "cpu",
        group_id=group_id,
        bootstrap_servers=BOOTSTRAP_SERVER,
    )
    for msg in consumer:
        print(msg.value)


def produce_to_cpu(producer_id: str) -> NoReturn:
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    while True:
        cpu_percent = psutil.cpu_percent()
        producer.send(
            "cpu",
            key=producer_id.encode(),
            value=json.dumps({"producer_id": producer_id, "cpu_percent": cpu_percent}).encode(),
        )
        time.sleep(0.5)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="subparser")
    producer_parser = subparsers.add_parser("producer")
    consumer_parser = subparsers.add_parser("consumer")
    args = parser.parse_args()

    match args.subparser:
        case "producer":
            produce_to_cpu("test_prod")
        case "consumer":
            consume_and_print("test")


if __name__ == "__main__":
    main()
