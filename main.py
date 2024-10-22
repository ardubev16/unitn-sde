#!/usr/bin/env python3

import argparse
import logging
import time
from random import choice, randint
from typing import NoReturn

import psutil
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(level=logging.INFO)
BOOTSTRAP_SERVER = "localhost:9094"


def consume_and_print(group_id: str) -> None:
    consumer = KafkaConsumer(
        "cpu",
        group_id=group_id,
        bootstrap_servers=BOOTSTRAP_SERVER,
    )
    for msg in consumer:
        print(msg)


def produce_counter() -> NoReturn:
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    possible_keys = ["key1", "key2", "key3", "key4"]
    counter = 0
    while True:
        cpu_percent = psutil.cpu_percent()
        producer.send(
            "cpu",
            key=choice(possible_keys).encode(),
            # partition=randint(0, 1),
            value=str(counter).encode(),
        )
        counter += 1
        time.sleep(0.01)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="subparser")
    producer_parser = subparsers.add_parser("producer")
    consumer_parser = subparsers.add_parser("consumer")
    args = parser.parse_args()

    match args.subparser:
        case "producer":
            produce_counter()
        case "consumer":
            consume_and_print("test")


if __name__ == "__main__":
    main()
