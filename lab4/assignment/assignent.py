import json
import sys
from pathlib import Path

from kafka import KafkaConsumer, KafkaProducer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER, USERNAME

ALPHA = 0.2


def main() -> None:
    """
    In this assignment you are required to write a consumer that processes the data from the "cpu" and "ram" topics.

    you will have to subscribe to two topics at once.

    for both cpu and ram, compute an exmponential moving average and push it it to respective topics: "cpu_avg" and "ram_avg"
    """
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    # TODO: Subscribe to two topics

    producer = KafkaProducer(bootstrap_servers=SERVER)

    cpu_avg = 0
    ram_avg = 0

    for msg in consumer:
        value = json.loads(msg.value.decode())

        if msg.topic == "cpu":
            cpu_avg = ...  # TODO: add formula

            # TODO: send the value in json (same format as exercise 1) to the topic "cpu_avg"
            # only care about cpu_percent, ignore n_processes

        else:
            ram_avg = ...  # TODO: add formula

            # TODO: send the value in json (same format as exercise 1) to the topic "ram_avg"


if __name__ == "__main__":
    main()
