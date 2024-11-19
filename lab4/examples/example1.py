import json
import sys
import time
from pathlib import Path
from typing import NoReturn

import psutil
from kafka import KafkaProducer  # kafka-python-ng library

# Add the parent folder to path so the common file can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER, USERNAME


def main() -> NoReturn:
    """Create a simple kafka producer that pushes CPU statistics to a broker."""
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
