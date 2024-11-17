from datetime import datetime

import cv2
import numpy as np
from common import SERVER
from kafka import KafkaConsumer


def consume_jpeg(consumer: KafkaConsumer) -> None:
    for msg in consumer:
        # convert compressed jpeg data to image matrix
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)

        timestamp = datetime.fromtimestamp(msg.timestamp/1000)

        print(timestamp)
        # show frame on screen
        cv2.imshow("Piazza Di Spagna", img)
        # delay for 1000 ms before showing next frame
        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break   # quit when q is pressed


if __name__ == "__main__":
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["jpeg"])
    consume_jpeg(consumer)
    cv2.destroyAllWindows()
