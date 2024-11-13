import json
import time
from typing import NoReturn

import psutil
from kafka import KafkaConsumer, KafkaProducer


def produce(producer: KafkaProducer, producer_id: str) -> NoReturn:
    while True:
        cpu_percent = psutil.cpu_percent()
        number_of_pids = len(psutil.pids())
        producer.send(
            "cpu",
            key=producer_id.encode(),
            value=json.dumps(
                {
                    "producer_id": producer_id,
                    "cpu_percent": cpu_percent,
                    "number_of_pids": number_of_pids,
                },
            ).encode(),
        )
        time.sleep(0.5)


def consume(consumer: KafkaConsumer) -> None:
    consumer.subscribe(["cpu"])
    for msg in consumer:
        print(msg.value.decode())
