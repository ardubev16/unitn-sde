import json
import time
from typing import NoReturn

import psutil
from kafka import KafkaProducer

from lab4.common import SERVER, USERNAME


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

        # Get RAM usage value
        ram_value = ...
        # Push RAM usage value to Queue

        value = json.dumps(
            {
                "producer_id": USERNAME,
                "memory": ram_value,
            },
        ).encode()

        time.sleep(0.5)


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=SERVER)
    publish_cpu_usage(producer)
