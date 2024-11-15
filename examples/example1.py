import json
import time
from typing import NoReturn

import psutil
from kafka import KafkaProducer

from ..common import SERVER, USERNAME


def publish_cpu_usage(producer: KafkaProducer) -> NoReturn:
    while True:
        cpu_percent = psutil.cpu_percent()
        n_processes = len(psutil.pids())
        producer.send(
            "cpu",
            key=USERNAME,
            value=json.dumps(
                {
                    "cpu_percent": cpu_percent,
                    "n_processes": n_processes,
                },
            ).encode(),
        )
        time.sleep(0.5)


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=SERVER)
    publish_cpu_usage(producer)
