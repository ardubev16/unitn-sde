import json
import sys
import time
from pathlib import Path
from typing import NoReturn

import psutil
from kafka import KafkaProducer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER, USERNAME


def main() -> NoReturn:
    """
    In this exercise you are required to write a producer that pushes two different kinds of information: CPU and RAM usage.

    The CPU code is already present and is the same from exercise 1

    You are simply required to add the code to also push the RAM usage (in bytes) to the "ram" topic.
    """
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

        ram_value = psutil.virtual_memory().used

        value = json.dumps(
            {
                "producer_id": USERNAME,
                "memory": ram_value,
            },
        ).encode()

        # TODO: push json value to the "ram" topic
        producer.send(
            topic="ram",
            key=USERNAME.encode(),
            value=value,
        )

        time.sleep(0.5)


if __name__ == "__main__":
    main()
