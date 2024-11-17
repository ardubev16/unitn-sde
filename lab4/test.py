from common import SERVER, USERNAME
from kafka import KafkaConsumer, KafkaProducer

if __name__ == "__main__":
    if USERNAME == "":
        msg = "Username was not set"
        raise ValueError(msg)

    print(f"Username: {USERNAME}, Server address: {SERVER}")

    producer = KafkaProducer(bootstrap_servers=SERVER)
    producer.send("test", key=USERNAME.encode())
    print("Producer test OK")

    consumer = KafkaConsumer("test", auto_offset_reset="earliest", bootstrap_servers=SERVER)
    test = next(consumer)

    if test:
        print("Consumer test OK")
