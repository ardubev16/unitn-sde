import json

from kafka import KafkaConsumer, KafkaProducer

from lab4.common import SERVER, USERNAME


def average_resource_util(consumer: KafkaConsumer, producer: KafkaProducer) -> None:
    cpu_buffer = 1
    ram_buffer = 1
    for msg in consumer:
        value = json.loads(msg.value.decode())

        if msg.topic == "cpu_avg":
            cpu_buffer = value["n_processes"]
        else:
            ram_buffer = value["ram"]

        result = ram_buffer / cpu_buffer
        value = json.dumps(
            {
                "process_avg_mem": result,
            },
        )
        producer.send(
            topic="process_ram_avg",
            key=USERNAME.encode(),
            value=value.encode,
        )


if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    producer = KafkaProducer(bootstrap_servers=SERVER)
    consumer.subscribe(["cpu_avg", "ram_avg"])
    average_resource_util(consumer, producer)
