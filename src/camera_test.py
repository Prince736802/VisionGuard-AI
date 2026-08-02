import cv2

print("OpenCV Version:", cv2.__version__)

camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

print("Camera opened:", camera.isOpened())

if camera.isOpened():
    ret, frame = camera.read()
    print("Frame captured:", ret)

camera.release()