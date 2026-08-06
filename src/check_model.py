from ultralytics import YOLO

print("Loading Helmet Model...")

model = YOLO("models/helmet.pt")

print("\n✅ Model Loaded Successfully\n")

print("Classes:\n")

for key, value in model.names.items():
    print(f"{key} : {value}")