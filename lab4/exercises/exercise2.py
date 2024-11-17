from datetime import datetime

import cv2
import numpy as np
from kafka import KafkaConsumer, KafkaProducer

from lab4.common import SERVER, USERNAME


def process_video(consumer: KafkaConsumer, producer: KafkaProducer) -> None:
    img1 = None

    for msg in consumer:
        # convert compressed jpeg data to image matrix
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)
        if img1 is None:
            img1 = img
            continue

        difference = cv2.subtract(img1, img)
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)

        # publish webcam motion (png compressed)
        producer.send(
            topic="webcam_motion",
            key=USERNAME.encode(),
            value=cv2.imencode(".png", thresh)[1],
        )

        # show frame on screen
        cv2.imshow("Piazza Di Spagna - Motion", thresh)
        # delay for 1000 ms before showing next frame
        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break  # quit when q is pressed


if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    producer = KafkaProducer(bootstrap_servers=SERVER)
    consumer.subscribe(["jpeg"])
    process_video(consumer, producer)
    cv2.destroyAllWindows()
