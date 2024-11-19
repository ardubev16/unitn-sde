import sys
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from kafka import KafkaConsumer

sys.path.append(str(Path(__file__).resolve().parents[2]))
from lab4.common import SERVER


def main() -> None:
    """Visualze video frames from a webcam on screen using cv2."""
    consumer = KafkaConsumer(group_id=None, bootstrap_servers=SERVER)
    consumer.subscribe(["webcam"])

    for msg in consumer:
        # convert compressed jpeg data to image matrix
        img = cv2.imdecode(np.frombuffer(msg.value, np.uint8), cv2.IMREAD_COLOR)

        timestamp = datetime.fromtimestamp(msg.timestamp / 1000)

        print(timestamp)
        # show frame on screen
        cv2.imshow("Piazza Di Spagna", img)
        # delay for 1000 ms before showing next frame
        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break  # quit when q is pressed
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
