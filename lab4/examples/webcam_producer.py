import os
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import NoReturn

import cv2
import ffmpeg
import requests
from kafka import KafkaProducer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER

INIT_URL = "https://hd-auth.skylinewebcams.com/live.m3u8?a=3thv677ivptnbchuie8jssdhv6"

def main() -> NoReturn:
    """
    This producer is already run by us we do not require students to run this file.

    This script uses ffmpeg and cv2 to extract frames from a publically available webcam and pushes them to kakfa
    """
    producer = KafkaProducer(bootstrap_servers=SERVER)
    while True:
        res_text = requests.get(INIT_URL, timeout=10).text
        latest_ts_url = res_text.splitlines()[-1]
        produce_jpegs_from_ts(producer, latest_ts_url)

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

            # Reduce resolution and compress image to save bandwidth
            image = cv2.imread(str(tmppath / img))
            image = cv2.resize(image, (854, 480))
            encoded_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1]

            producer.send("webcam", value=encoded_image.tobytes())
    time.sleep(4)


if __name__ == "__main__":
    main()
