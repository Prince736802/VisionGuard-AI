import cv2
from ultralytics import YOLO


def main():
    print("Loading YOLO model...")

    # Load YOLOv8 Nano model
    model = YOLO("yolov8n.pt")

    # Open default webcam
    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not camera.isOpened():
        print("Unable to open camera.")
        return

    print("Camera started successfully.")
    print("Press 'Q' to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Unable to read frame.")
            break

        # Run detection with confidence threshold
        results = model(frame, conf=0.60, verbose=False)

        # Draw YOLO detections
        output_frame = results[0].plot()

        # Count only persons
        person_count = 0

        for box in results[0].boxes:
            class_id = int(box.cls[0])

            if class_id == 0:
                person_count += 1

        # Display project title
        cv2.putText(
            output_frame,
            "VisionGuard AI",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display person count
        cv2.putText(
            output_frame,
            f"Persons: {person_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Show output
        cv2.imshow("VisionGuard AI", output_frame)

        # Exit on Q key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()