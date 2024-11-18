import sys
from pathlib import Path

import cv2
import numpy as np
from kafka import KafkaConsumer, KafkaProducer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER, USERNAME

"""
    In this exercise you are required to write a consumer that processes images from the webcam stream

    The images are read from the "webcam" topic and the processes images need to be pushed to the
    "webcam_motion" topic.

    The processing code is already present, you will simply have to add the kafka code yourself to make it work.
"""


def main() -> None:
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["webcam"])
    # TODO: subcribe to webcam stream

    producer = KafkaProducer(bootstrap_servers=SERVER)

    img1 = None
    for msg in consumer:
        # convert compressed jpeg data to image matrix
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)

        # initialize the buffer of the image frame
        if img1 is None:
            img1 = img
            continue

        # using cv2 extract the motion
        difference = np.abs(cv2.subtract(img1, img))
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)[1]


        # compress the image and covert it to bytes
        value = cv2.imencode(".png", thresh)[1].tobytes()

        # TODO: publish result to "webcam_motion" topic
        producer.send(
            topic="webcam_motion",
            key=USERNAME.encode(),
            value=value,
        )

        # show frame on screen
        cv2.imshow("Piazza Di Spagna - Motion", thresh)
        # delay for 1000 ms before showing next frame
        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break  # quit when q is pressed
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
