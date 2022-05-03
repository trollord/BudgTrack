# security  feature to prevent brute force attack
import time
import cv2
from time import sleep


def theft_detection():
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            cv2.imwrite(filename='capture.jpg', img=frame)
            webcam.release()
            break
        except:
            pass
