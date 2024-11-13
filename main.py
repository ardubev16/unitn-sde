#!/usr/bin/env python3

import argparse
import json
import logging
import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import NoReturn

import cv2
import ffmpeg
import numpy as np
import psutil
import requests
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(level=logging.INFO)
TOPICS = ["cpu", "jpeg"]
REMOTE_SERVER = "172.31.199.2:9094"
LOCAL_SERVER = "localhost:9094"


def produce_to_cpu(producer: KafkaProducer, producer_id: str) -> NoReturn:
    while True:
        cpu_percent = psutil.cpu_percent()
        producer.send(
            "cpu",
            key=producer_id.encode(),
            value=json.dumps({"producer_id": producer_id, "cpu_percent": cpu_percent}).encode(),
        )
        time.sleep(0.5)


def consume_cpu(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["cpu"])
    for msg in consumer:
        print(msg.value.decode())


def produce_jpegs_from_ts(producer: KafkaProducer, ts_url: str) -> None:
    print(f"Fetching url: {ts_url}")
    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        try:
            ffmpeg.FFmpeg().input(ts_url).output(
                tmppath / "frame_%03d.jpg",
                vf="fps=1",
                qscale=2,
            ).execute()
        except ffmpeg.errors.FFmpegError as e:
            print(f"FFmpeg error: {e}")
            return

        for img in os.listdir(tmppath):
            print(f"\tSending img: {img}")
            with (tmppath / img).open("rb") as f:
                producer.send("jpeg", value=f.read())
    time.sleep(4)


def produce_to_jpeg(producer: KafkaProducer, init_url: str) -> NoReturn:
    while True:
        res_text = requests.get(init_url, timeout=10).text
        latest_ts_url = res_text.splitlines()[-1]
        produce_jpegs_from_ts(producer, latest_ts_url)


def consume_jpeg(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["jpeg"])
    for msg in consumer:
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Live Feed", img)
        cv2.waitKey(1100)

    cv2.destroyAllWindows()


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

    match args.subparser:
        case "producer":
            producer = KafkaProducer(bootstrap_servers=bootstrap_server)
            if args.topic == "cpu":
                produce_to_cpu(producer, "test_prod")
            elif args.topic == "jpeg":
                produce_to_jpeg(producer, "https://hd-auth.skylinewebcams.com/live.m3u8?a=iomkvtaeogle92ctjjr9c8r770")

        case "consumer":
            consumer = KafkaConsumer(group_id=args.groupid, bootstrap_servers=bootstrap_server)
            if args.topic == "cpu":
                consume_cpu(consumer)
            elif args.topic == "jpeg":
                consume_jpeg(consumer)


if __name__ == "__main__":
    main()
