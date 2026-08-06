from ultralytics import YOLO


class PersonDetector:

    def __init__(self):
        print("Loading Person Detection Model...")
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        results = self.model(
            frame,
            conf=0.60,
            verbose=False
        )

        return results