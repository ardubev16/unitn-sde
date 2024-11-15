from datetime import datetime

import cv2
import numpy as np
from kafka import KafkaConsumer

from ..common import SERVER


def consume_jpeg(consumer: KafkaConsumer) -> None:
    for msg in consumer:
        # convert compressed jpeg data to image matrix
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)

        timestamp = datetime.fromtimestamp(msg.timestamp)

        # show frame on screen
        cv2.imshow(f"Piazza Di Spagna {timestamp.isoformat()}", img)
        # delay for 30 ms before showing next frame
        cv2.waitKey(30)

if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["webcam"])
    consume_jpeg(consumer)
    cv2.destroyAllWindows()
