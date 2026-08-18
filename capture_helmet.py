import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Camera open nahi hua")
    exit()

print("Camera open ho gaya.")
print("Helmet pehenkar camera ke saamne raho.")
print("5 seconds baad photo automatically save hogi.")

start = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    elapsed = time.time() - start

    cv2.putText(
        frame,
        f"Capture in: {max(0, 5 - int(elapsed))}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Helmet Test Capture", frame)

    if elapsed >= 5:
        cv2.imwrite("helmet_test.jpg", frame)
        print("Saved: helmet_test.jpg")
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()