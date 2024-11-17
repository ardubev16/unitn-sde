import json

from kafka import KafkaConsumer

from lab4.common import SERVER


def read_cpu_usage(consumer: KafkaConsumer) -> None:
    for msg in consumer:
        user = msg.key.decode()
        value = json.loads(msg.value.decode())
        print(f"{user}: CPU usage: {value['cpu_percent']: 02.1f}%, {value['n_processes']} processes running.")


if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["cpu"])
    read_cpu_usage(consumer)
