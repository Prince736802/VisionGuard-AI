import cv2
import time
import os
from ultralytics import YOLO
from logger import save_log

def main():
    print("Loading YOLO model...")

    # Load YOLOv8 Nano model
    model = YOLO("yolov8n.pt")

    # Create screenshots folder
    os.makedirs("screenshots", exist_ok=True)

    # Open webcam
    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not camera.isOpened():
        print("Unable to open camera.")
        return

    print("Camera started successfully.")
    print("Press 'S' to save screenshot.")
    print("Press 'Q' to quit.")

    previous_time = time.time()

    while True:

        success, frame = camera.read()

        if not success:
            print("Unable to read frame.")
            break

        # Run YOLO detection
        results = model(frame, conf=0.60, verbose=False)

        # Draw detection boxes
        output_frame = results[0].plot()

        # Count only persons
        person_count = 0

        for box in results[0].boxes:
            class_id = int(box.cls[0])

            if class_id == 0:
                person_count += 1
                
# Save detection log
                save_log(person_count)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Title
        cv2.putText(
            output_frame,
            "VisionGuard AI",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Person Count
        cv2.putText(
            output_frame,
            f"Persons: {person_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # FPS
        cv2.putText(
            output_frame,
            f"FPS: {int(fps)}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Show camera
        cv2.imshow("VisionGuard AI", output_frame)

        key = cv2.waitKey(1) & 0xFF

        # Save screenshot
        if key == ord("s"):
            filename = os.path.join(
                "screenshots",
                f"screenshot_{int(time.time())}.jpg"
            )

            cv2.imwrite(filename, output_frame)
            print(f"Screenshot saved: {filename}")

        # Quit
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()