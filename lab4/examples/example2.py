import json
import sys
from pathlib import Path

from kafka import KafkaConsumer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER


def main() -> None:
    """Create a simple kafka consumer that prints to the screen the cpu statics of all students on the screen."""
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["cpu"])

    for msg in consumer:
        user = msg.key.decode()
        value = json.loads(msg.value.decode())
        print(f"{user}: CPU usage: {value['cpu_percent']: .2f}%, {value['n_processes']} processes running.")


if __name__ == "__main__":
    main()
