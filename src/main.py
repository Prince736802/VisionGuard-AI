import cv2
import time
import os
from collections import defaultdict, deque
from ultralytics import YOLO


# =========================================================
# CONFIGURATION
# =========================================================

PERSON_MODEL = "yolov8n.pt"
HELMET_MODEL = "models/helmet.pt"

PERSON_CONF = 0.45

HELMET_CONF = 0.05

WITH_HELMET_THRESHOLD = 0.10
WITHOUT_HELMET_THRESHOLD = 0.18

HEAD_REGION_RATIO = 0.45

HISTORY_SIZE = 8

WITH_HELMET_VOTES = 4
WITHOUT_HELMET_VOTES = 4

MAX_MISSING_FRAMES = 6


# =========================================================
# CREATE DIRECTORIES
# =========================================================

os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# =========================================================
# SCREENSHOT
# =========================================================

def save_screenshot(frame, person_id):

    filename = (
        f"screenshots/"
        f"person_{person_id}_"
        f"{int(time.time())}.jpg"
    )

    cv2.imwrite(filename, frame)

    print(f"Screenshot saved: {filename}")


# =========================================================
# LOG
# =========================================================

def save_violation_log(person_id):

    os.makedirs("logs", exist_ok=True)

    filename = "logs/helmet_violations.csv"

    new_file = not os.path.exists(filename)

    with open(filename, "a") as f:

        if new_file:
            f.write("timestamp,person_id,violation\n")

        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')},"
            f"{person_id},"
            f"NO HELMET\n"
        )

    print(
        f"Violation logged: Person {person_id}"
    )


# =========================================================
# PERSON BOX VALIDATION
# =========================================================

def valid_person_box(x1, y1, x2, y2):

    width = x2 - x1
    height = y2 - y1

    if width < 70:
        return False

    if height < 120:
        return False

    aspect_ratio = (
        width /
        max(height, 1)
    )

    if aspect_ratio < 0.20:
        return False

    if aspect_ratio > 2.20:
        return False

    return True


# =========================================================
# HELMET BOX VALIDATION
# =========================================================

def valid_helmet_box(
    box,
    roi_width,
    roi_height
):

    hx1, hy1, hx2, hy2 = box

    box_width = hx2 - hx1
    box_height = hy2 - hy1

    if box_width <= 0:
        return False

    if box_height <= 0:
        return False

    if box_width < roi_width * 0.05:
        return False

    if box_height < roi_height * 0.03:
        return False

    center_y = (
        hy1 + hy2
    ) / 2

    center_ratio = (
        center_y /
        max(roi_height, 1)
    )

    if center_ratio > 0.90:
        return False

    return True


# =========================================================
# HELMET DETECTION
# =========================================================

def detect_helmet(
    helmet_model,
    head_crop
):

    if head_crop is None or head_crop.size == 0:
        return None

    roi_height, roi_width = head_crop.shape[:2]

    results = helmet_model(
        head_crop,
        conf=HELMET_CONF,
        iou=0.45,
        imgsz=640,
        max_det=3,
        verbose=False
    )

    result = results[0]

    if result.boxes is None or len(result.boxes) == 0:
        return None

    best_by_class = {
        0: None,
        1: None
    }

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id not in (0, 1):
            continue

        hx1, hy1, hx2, hy2 = map(
            int,
            box.xyxy[0]
        )

        current_box = (
            hx1,
            hy1,
            hx2,
            hy2
        )

        if not valid_helmet_box(
            current_box,
            roi_width,
            roi_height
        ):
            continue

        threshold = (
            WITH_HELMET_THRESHOLD
            if class_id == 0
            else WITHOUT_HELMET_THRESHOLD
        )

        if confidence < threshold:
            continue

        old = best_by_class[class_id]

        if old is None or confidence > old["confidence"]:

            best_by_class[class_id] = {
                "class": class_id,
                "confidence": confidence,
                "box": current_box
            }

    with_det = best_by_class[0]
    without_det = best_by_class[1]

    if with_det is None and without_det is None:
        return None

    if with_det is not None and without_det is None:
        return with_det

    if without_det is not None and with_det is None:
        return without_det

    with_conf = with_det["confidence"]
    without_conf = without_det["confidence"]

    margin = 0.05

    if with_conf >= without_conf + margin:
        return with_det

    if without_conf >= with_conf + margin:
        return without_det

    return None


# =========================================================
# STATUS CALCULATION
# =========================================================

def calculate_status(state):

    history = state["history"]

    if len(history) < 3:
        return "Checking..."

    with_votes = history.count(
        "With Helmet"
    )

    without_votes = history.count(
        "Without Helmet"
    )

    if (
        with_votes >= WITH_HELMET_VOTES
        and with_votes > without_votes
    ):

        state["status"] = "With Helmet"

        return "With Helmet"

    if (
        without_votes >= WITHOUT_HELMET_VOTES
        and without_votes > with_votes
    ):

        state["status"] = "Without Helmet"

        return "Without Helmet"

    return "Checking..."


# =========================================================
# UPDATE PERSON STATE
# =========================================================

def update_person_state(
    state,
    detection
):

    history = state["history"]

    if detection is None:

        state["missing_frames"] += 1

        if (
            state["missing_frames"]
            >= MAX_MISSING_FRAMES
        ):

            history.clear()

            state["status"] = "Checking..."

        return "Checking..."

    state["missing_frames"] = 0

    class_id = detection["class"]
    confidence = detection["confidence"]

    if class_id == 0:

        if (
            confidence
            >= WITH_HELMET_THRESHOLD
        ):

            history.append(
                "With Helmet"
            )

    elif class_id == 1:

        if (
            confidence
            >= WITHOUT_HELMET_THRESHOLD
        ):

            history.append(
                "Without Helmet"
            )

    return calculate_status(state)


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("======================================")
    print("          VisionGuard AI")
    print("======================================")
    print()

    print(
        "Loading Person Detection Model..."
    )

    person_model = YOLO(
        PERSON_MODEL
    )

    print(
        "Loading Helmet Detection Model..."
    )

    helmet_model = YOLO(
        HELMET_MODEL
    )

    print()
    print("Helmet Classes:")

    for class_id, name in (
        helmet_model.names.items()
    ):

        print(
            f"  {class_id}: {name}"
        )

    print()
    print(
        "Both models loaded successfully."
    )

    print()
    print(
        "Starting camera..."
    )

    print(
        "Press Q to quit."
    )

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_AVFOUNDATION
    )

    if not camera.isOpened():

        print(
            "ERROR: Camera not opened."
        )

        return

    print(
        "Camera Started"
    )

    previous_time = time.time()

    person_states = defaultdict(
        lambda: {

            "history": deque(
                maxlen=HISTORY_SIZE
            ),

            "missing_frames": 0,

            "status": "Checking...",

            "alert_sent": False
        }
    )

    while True:

        success, frame = camera.read()

        if not success:

            print(
                "Unable to read frame."
            )

            break

        frame_height, frame_width = (
            frame.shape[:2]
        )

        output_frame = frame.copy()

        # =================================================
        # PERSON TRACKING
        # =================================================

        results = person_model.track(

            frame,

            persist=True,

            tracker="bytetrack.yaml",

            classes=[0],

            conf=PERSON_CONF,

            imgsz=416,

            verbose=False
        )

        result = results[0]

        person_count = 0

        # =================================================
        # PROCESS PERSONS
        # =================================================

        if (
            result.boxes is not None
            and len(result.boxes) > 0
        ):

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                if class_id != 0:
                    continue

                if box.id is None:
                    continue

                person_id = int(
                    box.id[0]
                )

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                x1 = max(
                    0,
                    x1
                )

                y1 = max(
                    0,
                    y1
                )

                x2 = min(
                    frame_width,
                    x2
                )

                y2 = min(
                    frame_height,
                    y2
                )

                if not valid_person_box(
                    x1,
                    y1,
                    x2,
                    y2
                ):
                    continue

                person_count += 1

                # PERSON BOX

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
                    (
                        x1,
                        max(
                            25,
                            y1 - 10
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 0, 0),
                    2
                )

                # PERSON CROP

                person_crop = frame[
                    y1:y2,
                    x1:x2
                ]

                if person_crop.size == 0:
                    continue

                crop_height, crop_width = (
                    person_crop.shape[:2]
                )

                if (
                    crop_height < 80
                    or crop_width < 40
                ):
                    continue

                # HEAD REGION

                head_height = max(
                    1,
                    int(
                        crop_height *
                        HEAD_REGION_RATIO
                    )
                )

                head_crop = person_crop[
                    0:head_height,
                    0:crop_width
                ]

                if head_crop.size == 0:
                    continue

                # ROI GUIDE

                cv2.rectangle(
                    output_frame,
                    (x1, y1),
                    (
                        x2,
                        min(
                            y2,
                            y1 + head_height
                        )
                    ),
                    (255, 255, 0),
                    1
                )

                # HELMET DETECTION

                helmet_detection = detect_helmet(
                    helmet_model,
                    head_crop
                )

                # STATE

                state = person_states[
                    person_id
                ]

                final_status = (
                    update_person_state(
                        state,
                        helmet_detection
                    )
                )

                # HELMET BOX

                if helmet_detection is not None:

                    hx1, hy1, hx2, hy2 = (
                        helmet_detection[
                            "box"
                        ]
                    )

                    confidence = (
                        helmet_detection[
                            "confidence"
                        ]
                    )

                    helmet_class = (
                        helmet_detection[
                            "class"
                        ]
                    )

                    hx1 += x1
                    hx2 += x1

                    hy1 += y1
                    hy2 += y1

                    if helmet_class == 0:

                        color = (
                            0,
                            255,
                            0
                        )

                        label = (
                            f"With Helmet "
                            f"{confidence:.2f}"
                        )

                    else:

                        color = (
                            0,
                            0,
                            255
                        )

                        label = (
                            f"Without Helmet "
                            f"{confidence:.2f}"
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
                        (
                            hx1,
                            max(
                                25,
                                hy1 - 10
                            )
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.60,
                        color,
                        2
                    )

                # STATUS POSITION

                status_y = y2 + 25

                if status_y >= frame_height:

                    status_y = max(
                        25,
                        y2 - 10
                    )

                # SAFE

                if final_status == (
                    "With Helmet"
                ):

                    status_color = (
                        0,
                        255,
                        0
                    )

                    status_text = (
                        f"ID {person_id}: SAFE"
                    )

                # NO HELMET

                elif final_status == (
                    "Without Helmet"
                ):

                    status_color = (
                        0,
                        0,
                        255
                    )

                    status_text = (
                        f"ID {person_id}: "
                        f"NO HELMET"
                    )

                # CHECKING

                else:

                    status_color = (
                        255,
                        255,
                        0
                    )

                    status_text = (
                        f"ID {person_id}: "
                        f"CHECKING"
                    )

                cv2.putText(
                    output_frame,
                    status_text,
                    (
                        x1,
                        status_y
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    status_color,
                    2
                )

                # =================================================
                # ALERT
                # =================================================

                # Helmet pehenne par alert reset
                if final_status == "With Helmet":
                    state["alert_sent"] = False

                if final_status == "Without Helmet":

                    cv2.putText(
                        output_frame,
                        "ALERT: NO HELMET!",
                        (20, 155),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 0, 255),
                        3
                    )

                    # Same person ke liye sirf ek baar
                    if not state["alert_sent"]:

                        save_screenshot(
                            output_frame,
                            person_id
                        )

                        save_violation_log(
                            person_id
                        )

                        state["alert_sent"] = True

                        print(
                            f"ALERT: Person "
                            f"{person_id} "
                            f"without helmet"
                        )

        # =====================================================
        # FPS
        # =====================================================

        current_time = time.time()

        time_difference = (
            current_time -
            previous_time
        )

        if time_difference > 0:

            fps = (
                1 /
                time_difference
            )

        else:

            fps = 0

        previous_time = current_time

        # =====================================================
        # PROJECT TITLE
        # =====================================================

        cv2.putText(
            output_frame,
            "VisionGuard AI",
            (
                20,
                40
            ),
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
            (
                20,
                80
            ),
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
            (
                20,
                115
            ),
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

        key = (
            cv2.waitKey(1)
            & 0xFF
        )

        if key == ord("q"):
            break

    # =====================================================
    # CLEANUP
    # =====================================================

    camera.release()

    cv2.destroyAllWindows()

    print()
    print(
        "VisionGuard AI stopped."
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()