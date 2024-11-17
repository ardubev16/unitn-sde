from kafka import KafkaConsumer, KafkaProducer

from lab4.common import SERVER, USERNAME

if __name__ == "__main__":
    print(f"Username: {USERNAME}, Server address: {SERVER}")

    producer = KafkaProducer(bootstrap_servers=SERVER)
    producer.send("test", key=USERNAME.encode())
    print("Producer test OK")

    consumer = KafkaConsumer("test", auto_offset_reset="earliest", bootstrap_servers=SERVER)
    test = next(consumer)

    if test:
        print("Consumer test OK")
