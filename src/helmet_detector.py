from ultralytics import YOLO


class HelmetDetector:

    def __init__(self):
        print("Loading Helmet Detection Model...")
        self.model = YOLO("models/helmet.pt")

    def detect(self, frame):

        results = self.model(
            frame,
            conf=0.50,
            verbose=False
        )

        return results