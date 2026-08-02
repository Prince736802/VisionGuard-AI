from ultralytics import YOLO

print("Loading model...")

model = YOLO("yolov8n.pt")

image_path = "https://ultralytics.com/images/bus.jpg"

results = model(image_path, save=True)

print("Detection completed.")