import json
import sys
from pathlib import Path

from kafka import KafkaConsumer, KafkaProducer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER, USERNAME


def main() -> None:
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    producer = KafkaProducer(bootstrap_servers=SERVER)
    consumer.subscribe(["cpu_avg", "ram_avg"])

    cpu_buffer = 1
    ram_buffer = 1

    for msg in consumer:
        value = json.loads(msg.value.decode())

        if msg.topic == "cpu_avg":
            cpu_buffer = value["n_processes"]
        else:
            ram_buffer = value["ram"]

        result = ram_buffer / cpu_buffer
        value = json.dumps({"process_avg_mem": result})

        producer.send(
            topic="process_ram_avg",
            key=USERNAME.encode(),
            value=value.encode(),
        )


if __name__ == "__main__":
    main()
