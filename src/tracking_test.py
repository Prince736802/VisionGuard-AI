import cv2
import time
from ultralytics import YOLO


def main():

    print("Loading YOLO model...")

    # Load YOLOv8 Nano model
    model = YOLO("yolov8n.pt")

    # Open webcam
    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not camera.isOpened():
        print("Camera not opened.")
        return

    print("Camera Started")
    print("Person Tracking Started")
    print("Press Q to Quit")

    previous_time = time.time()

    while True:

        # Read frame
        success, frame = camera.read()

        if not success:
            print("Unable to read frame.")
            break

        # --------------------------------
        # PERSON DETECTION + TRACKING
        # --------------------------------
        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],       # Only person
            conf=0.60,
            verbose=False
        )

        result = results[0]

        # Draw tracking results
        output_frame = result.plot()

        # --------------------------------
        # COUNT PERSONS
        # --------------------------------
        person_count = 0

        if result.boxes is not None:

            person_count = len(result.boxes)

            for box in result.boxes:

                # Class ID
                class_id = int(box.cls[0])

                # Only person
                if class_id != 0:
                    continue

                # Confidence
                confidence = float(box.conf[0])

                # Tracking ID
                if box.id is not None:
                    track_id = int(box.id[0])
                else:
                    track_id = -1

                print(
                    f"Person ID: {track_id} | "
                    f"Confidence: {confidence:.2f}"
                )

        # --------------------------------
        # FPS
        # --------------------------------
        current_time = time.time()

        time_difference = current_time - previous_time

        if time_difference > 0:
            fps = 1 / time_difference
        else:
            fps = 0

        previous_time = current_time

        # --------------------------------
        # PROJECT TITLE
        # --------------------------------
        cv2.putText(
            output_frame,
            "VisionGuard AI",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # --------------------------------
        # PERSON COUNT
        # --------------------------------
        cv2.putText(
            output_frame,
            f"Persons: {person_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # --------------------------------
        # FPS DISPLAY
        # --------------------------------
        cv2.putText(
            output_frame,
            f"FPS: {int(fps)}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # --------------------------------
        # DISPLAY
        # --------------------------------
        cv2.imshow(
            "VisionGuard AI - Person Tracking",
            output_frame
        )

        # --------------------------------
        # QUIT
        # --------------------------------
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # --------------------------------
    # RELEASE CAMERA
    # --------------------------------
    camera.release()
    cv2.destroyAllWindows()

    print("Tracking stopped.")


if __name__ == "__main__":
    main()