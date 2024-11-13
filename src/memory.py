import json
import time
from typing import NoReturn

import psutil
from kafka import KafkaConsumer, KafkaProducer


def ex1_produce(producer: KafkaProducer, producer_id: str) -> NoReturn:
    while True:
        used_memory = psutil.virtual_memory().used
        producer.send(
            "memory",
            key=producer_id.encode(),
            value=json.dumps({"producer_id": producer_id, "used_memory": used_memory}).encode(),
        )
        time.sleep(1)


def consume(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["memory"])
    for msg in consumer:
        print(msg.value.decode())
