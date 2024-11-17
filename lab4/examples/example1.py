import json
import time
from typing import NoReturn

import psutil
from kafka import KafkaProducer

from lab4.common import SERVER, USERNAME


def main() -> NoReturn:
    producer = KafkaProducer(bootstrap_servers=SERVER)

    while True:
        cpu_percent = psutil.cpu_percent()
        n_processes = len(psutil.pids())

        print(cpu_percent, n_processes)

        value = json.dumps(
            {
                "producer_id": USERNAME,
                "cpu_percent": cpu_percent,
                "n_processes": n_processes,
            },
        )

        producer.send(
            topic="cpu",
            key=USERNAME.encode(),
            value=value.encode(),
        )
        time.sleep(0.5)


if __name__ == "__main__":
    main()
