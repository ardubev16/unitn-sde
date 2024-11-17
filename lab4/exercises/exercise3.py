import json

from kafka import KafkaConsumer, KafkaProducer

from lab4.common import SERVER, USERNAME

ALPHA = 0.2


def average_resource_util(consumer: KafkaConsumer, producer: KafkaProducer) -> None:
    cpu_avg = 0
    processes_avg = 0
    ram_avg = 0

    for msg in consumer:
        value = json.loads(msg.value.decode())

        if msg.topic == "cpu":
            cpu_avg = cpu_avg * (1 - ALPHA) + value["cpu_percent"] * ALPHA
            processes_avg = processes_avg * (1 - ALPHA) + value["n_processes"] * ALPHA
            value = json.dumps(
                {
                    "cpu_percent": cpu_avg,
                    "n_processes": processes_avg,
                },
            )

            producer.send(
                topic="cpu_avg",
                key=USERNAME.encode(),
                value=value.encode(),
            )

        else:
            ram_avg = ram_avg * (1 - ALPHA) + value["memory"] * ALPHA
            value = json.dumps(
                {
                    "memory": ram_avg,
                },
            )

            producer.send(
                topic="memory_avg",
                key=USERNAME.encode(),
                value=value.encode(),
            )


if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    producer = KafkaProducer(bootstrap_servers=SERVER)
    consumer.subscribe(["cpu", "ram"])
    average_resource_util(consumer, producer)
