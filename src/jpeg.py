import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import NoReturn

import cv2
import ffmpeg
import numpy as np
import requests
from kafka import KafkaConsumer, KafkaProducer


def _produce_jpegs_from_ts(producer: KafkaProducer, ts_url: str) -> None:
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


def produce(producer: KafkaProducer, init_url: str) -> NoReturn:
    while True:
        res_text = requests.get(init_url, timeout=10).text
        latest_ts_url = res_text.splitlines()[-1]
        _produce_jpegs_from_ts(producer, latest_ts_url)


def consume(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["jpeg"])
    for msg in consumer:
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Live Feed", img)
        cv2.waitKey(1100)

    cv2.destroyAllWindows()
