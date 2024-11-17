import json
import time
from typing import NoReturn

import psutil
from common import SERVER, USERNAME
from kafka import KafkaProducer


def publish_cpu_usage(producer: KafkaProducer) -> NoReturn:
    while True:
        cpu_percent = psutil.cpu_percent()
        n_processes = len(psutil.pids())

        print(cpu_percent, n_processes)

        producer.send(
            topic="cpu",
            key=USERNAME.encode(),
            value=json.dumps(
                {
                    "producer_id": USERNAME,
                    "cpu_percent": cpu_percent,
                    "n_processes": n_processes,
                },
            ).encode(),
        )
        time.sleep(0.5)


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=SERVER)
    publish_cpu_usage(producer)
