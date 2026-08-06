import cv2
import time
import os

from person_detector import PersonDetector
from helmet_detector import HelmetDetector
from logger import save_log


def main():

    person_detector = PersonDetector()
    helmet_detector = HelmetDetector()

    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not camera.isOpened():
        print("Camera not opened.")
        return

    print("Camera Started")
    print("Press Q to Quit")

    os.makedirs("screenshots", exist_ok=True)

    last_alert_time = 0
    ALERT_COOLDOWN = 5

    while True:

        success, frame = camera.read()

        if not success:
            break

        output_frame = frame.copy()

        person_results = person_detector.detect(frame)

        person_count = 0

        for box in person_results[0].boxes:

            class_id = int(box.cls[0])

            if class_id != 0:
                continue

            person_count += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(
                output_frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            cv2.putText(
                output_frame,
                "Person",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

            person_crop = frame[y1:y2, x1:x2]

            if person_crop.size == 0:
                continue

            helmet_results = helmet_detector.detect(person_crop)

            for hbox in helmet_results[0].boxes:

                helmet_class = int(hbox.cls[0])

                hx1, hy1, hx2, hy2 = map(int, hbox.xyxy[0])

                hx1 += x1
                hx2 += x1
                hy1 += y1
                hy2 += y1

                if helmet_class == 0:

                    color = (0, 255, 0)
                    label = "With Helmet"

                else:

                    color = (0, 0, 255)
                    label = "Without Helmet"

                    cv2.putText(
                        output_frame,
                        "ALERT : NO HELMET DETECTED",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                    current_time = time.time()

                    if current_time - last_alert_time > ALERT_COOLDOWN:

                        filename = os.path.join(
                            "screenshots",
                            f"violation_{int(current_time)}.jpg"
                        )

                        cv2.imwrite(filename, output_frame)

                        save_log(person_count)

                        print(f"Violation Saved : {filename}")

                        last_alert_time = current_time

                cv2.rectangle(
                    output_frame,
                    (hx1, hy1),
                    (hx2, hy2),
                    color,
                    2
                )

                cv2.putText(
                    output_frame,
                    label,
                    (hx1, hy1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

        cv2.putText(
            output_frame,
            f"Persons : {person_count}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow("VisionGuard AI", output_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()