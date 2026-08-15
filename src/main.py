import cv2
import time
import os
import csv
from collections import defaultdict, deque
from datetime import datetime
from ultralytics import YOLO


# =========================================================
# CONFIGURATION
# =========================================================

PERSON_MODEL = "yolov8n.pt"
HELMET_MODEL = "models/helmet.pt"

PERSON_CONF = 0.60
HELMET_CONF = 0.75

SCREENSHOT_FOLDER = "screenshots"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "helmet_violations.csv")

# Only upper part of person is used for helmet detection
HEAD_REGION_RATIO = 0.50

# Number of recent predictions used for smoothing
HISTORY_SIZE = 7

# Minimum votes required for a final decision
MIN_VOTES = 4

# Alert screenshot cooldown
ALERT_COOLDOWN = 5


# =========================================================
# FOLDERS
# =========================================================

os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)


# =========================================================
# LOG VIOLATION
# =========================================================

def save_violation_log(person_id):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "Person_ID",
                "Status"
            ])

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        writer.writerow([
            current_time,
            person_id,
            "Without Helmet"
        ])


# =========================================================
# SAVE SCREENSHOT
# =========================================================

def save_screenshot(frame, person_id):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = os.path.join(
        SCREENSHOT_FOLDER,
        f"no_helmet_person_{person_id}_{timestamp}.jpg"
    )

    cv2.imwrite(filename, frame)

    print(f"Screenshot saved: {filename}")


# =========================================================
# MAIN
# =========================================================

def main():

    print("Loading Person Detection Model...")
    person_model = YOLO(PERSON_MODEL)

    print("Loading Helmet Detection Model...")
    helmet_model = YOLO(HELMET_MODEL)

    print()
    print("Both models loaded successfully.")
    print()
    print("Starting camera...")
    print("Press Q to quit.")

    # =====================================================
    # CAMERA
    # =====================================================

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_AVFOUNDATION
    )

    if not camera.isOpened():

        print("Camera not opened.")
        return

    print("Camera Started")

    previous_time = time.time()

    # =====================================================
    # TRACKING STATUS
    # =====================================================

    status_history = defaultdict(
        lambda: deque(maxlen=HISTORY_SIZE)
    )

    last_alert_time = {}

    # =====================================================
    # MAIN LOOP
    # =====================================================

    while True:

        success, frame = camera.read()

        if not success:

            print("Unable to read frame.")
            break

        # =================================================
        # PERSON DETECTION + TRACKING
        # =================================================

        results = person_model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=PERSON_CONF,
            verbose=False
        )

        result = results[0]

        output_frame = frame.copy()

        person_count = 0

        # =================================================
        # PERSON PROCESSING
        # =================================================

        if result.boxes is not None:

            person_count = len(result.boxes)

            for box in result.boxes:

                class_id = int(box.cls[0])

                if class_id != 0:
                    continue

                confidence = float(box.conf[0])

                # -----------------------------------------
                # TRACK ID
                # -----------------------------------------

                if box.id is not None:

                    person_id = int(box.id[0])

                else:

                    person_id = -1

                # -----------------------------------------
                # PERSON BOX
                # -----------------------------------------

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                height, width = frame.shape[:2]

                x1 = max(0, x1)
                y1 = max(0, y1)

                x2 = min(width, x2)
                y2 = min(height, y2)

                if x2 <= x1 or y2 <= y1:
                    continue

                # -----------------------------------------
                # PERSON BOX
                # -----------------------------------------

                cv2.rectangle(
                    output_frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    output_frame,
                    f"Person ID: {person_id}",
                    (x1, max(25, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 0, 0),
                    2
                )

                # =================================================
                # HEAD / UPPER-BODY ROI
                # =================================================

                person_crop = frame[
                    y1:y2,
                    x1:x2
                ]

                crop_height, crop_width = person_crop.shape[:2]

                if crop_height < 40 or crop_width < 40:
                    continue

                # Only upper 50% of person
                head_height = int(
                    crop_height * HEAD_REGION_RATIO
                )

                head_crop = person_crop[
                    0:head_height,
                    0:crop_width
                ]

                if head_crop.size == 0:
                    continue

                # =================================================
                # HELMET DETECTION
                # =================================================

                helmet_results = helmet_model(
                    head_crop,
                    conf=HELMET_CONF,
                    verbose=False
                )

                helmet_result = helmet_results[0]

                frame_status = None

                best_confidence = 0.0
                best_box = None
                best_class = None

                # =================================================
                # PROCESS HELMET DETECTIONS
                # =================================================

                if helmet_result.boxes is not None:

                    for helmet_box in helmet_result.boxes:

                        helmet_class = int(
                            helmet_box.cls[0]
                        )

                        helmet_confidence = float(
                            helmet_box.conf[0]
                        )

                        hx1, hy1, hx2, hy2 = map(
                            int,
                            helmet_box.xyxy[0]
                        )

                        # Keep only strongest detection
                        if helmet_confidence > best_confidence:

                            best_confidence = helmet_confidence
                            best_box = (
                                hx1,
                                hy1,
                                hx2,
                                hy2
                            )
                            best_class = helmet_class

                # =================================================
                # CURRENT FRAME STATUS
                # =================================================

                if best_class is not None:

                    if best_class == 0:

                        frame_status = "With Helmet"

                    elif best_class == 1:

                        frame_status = "Without Helmet"

                # =================================================
                # TEMPORAL SMOOTHING
                # =================================================

                if frame_status is not None:

                    status_history[person_id].append(
                        frame_status
                    )

                history = status_history[person_id]

                final_status = "Checking..."

                if len(history) >= MIN_VOTES:

                    with_helmet_votes = history.count(
                        "With Helmet"
                    )

                    without_helmet_votes = history.count(
                        "Without Helmet"
                    )

                    # -----------------------------------------
                    # WITH HELMET
                    # -----------------------------------------

                    if (
                        with_helmet_votes
                        >= MIN_VOTES
                        and with_helmet_votes
                        > without_helmet_votes
                    ):

                        final_status = "With Helmet"

                    # -----------------------------------------
                    # WITHOUT HELMET
                    # -----------------------------------------

                    elif (
                        without_helmet_votes
                        >= MIN_VOTES
                        and without_helmet_votes
                        > with_helmet_votes
                    ):

                        final_status = "Without Helmet"

                # =================================================
                # DRAW HELMET BOX
                # =================================================

                if best_box is not None:

                    hx1, hy1, hx2, hy2 = best_box

                    # Convert head ROI coordinates
                    # back to original frame
                    hx1 += x1
                    hx2 += x1
                    hy1 += y1
                    hy2 += y1

                    if final_status == "With Helmet":

                        color = (0, 255, 0)

                        label = (
                            f"With Helmet "
                            f"{best_confidence:.2f}"
                        )

                    elif final_status == "Without Helmet":

                        color = (0, 0, 255)

                        label = (
                            f"Without Helmet "
                            f"{best_confidence:.2f}"
                        )

                    else:

                        color = (255, 255, 0)

                        label = (
                            f"Checking "
                            f"{best_confidence:.2f}"
                        )

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
                        (hx1, max(25, hy1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        color,
                        2
                    )

                # =================================================
                # STATUS FOR PERSON
                # =================================================

                status_y = y2 + 25

                if status_y >= height:
                    status_y = y2 - 10

                if final_status == "With Helmet":

                    status_color = (0, 255, 0)

                    status_text = (
                        f"ID {person_id}: SAFE"
                    )

                elif final_status == "Without Helmet":

                    status_color = (0, 0, 255)

                    status_text = (
                        f"ID {person_id}: NO HELMET"
                    )

                else:

                    status_color = (255, 255, 0)

                    status_text = (
                        f"ID {person_id}: CHECKING"
                    )

                cv2.putText(
                    output_frame,
                    status_text,
                    (x1, status_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    status_color,
                    2
                )

                # =================================================
                # ALERT
                # =================================================

                if final_status == "Without Helmet":

                    current_time = time.time()

                    last_time = last_alert_time.get(
                        person_id,
                        0
                    )

                    cv2.putText(
                        output_frame,
                        "ALERT: NO HELMET!",
                        (20, 155),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 0, 255),
                        3
                    )

                    # Save only once every few seconds
                    if (
                        current_time - last_time
                        >= ALERT_COOLDOWN
                    ):

                        save_screenshot(
                            output_frame,
                            person_id
                        )

                        save_violation_log(
                            person_id
                        )

                        last_alert_time[
                            person_id
                        ] = current_time

                        print(
                            f"ALERT: Person {person_id} "
                            f"without helmet"
                        )

        # =====================================================
        # FPS
        # =====================================================

        current_time = time.time()

        time_difference = (
            current_time - previous_time
        )

        if time_difference > 0:

            fps = 1 / time_difference

        else:

            fps = 0

        previous_time = current_time

        # =====================================================
        # PROJECT TITLE
        # =====================================================

        cv2.putText(
            output_frame,
            "VisionGuard AI",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # =====================================================
        # PERSON COUNT
        # =====================================================

        cv2.putText(
            output_frame,
            f"Persons: {person_count}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # =====================================================
        # FPS
        # =====================================================

        cv2.putText(
            output_frame,
            f"FPS: {int(fps)}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # =====================================================
        # DISPLAY
        # =====================================================

        cv2.imshow(
            "VisionGuard AI",
            output_frame
        )

        # =====================================================
        # QUIT
        # =====================================================

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # =========================================================
    # CLEANUP
    # =========================================================

    camera.release()
    cv2.destroyAllWindows()

    print()
    print("VisionGuard AI stopped.")


if __name__ == "__main__":
    main()