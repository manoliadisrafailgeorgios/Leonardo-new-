import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 10)

prev_gray = None

def detect_face():
    global prev_gray
    if not cap.isOpened():
        return False, 0, 0, False

    for _ in range(4):
        cap.grab()

    ret, frame = cap.read()
    if not ret:
        return False, 0, 0, False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    is_waving = False
    dx, dy = 0, 0

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        
        # Calculate exact center of your face
        cx = x + w // 2
        cy = y + h // 2
        
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

        # Map face position to eye movement limits
        offset_x = cx - frame_center_x
        offset_y = cy - frame_center_y
        
        dx = int((offset_x / frame_center_x) * 50)
        dy = int((offset_y / frame_center_y) * 20)
        
        # Wave Detection: Look for motion next to the face
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            
            # Scan the area to the left and right of your head
            left_box = thresh[max(0, y):min(frame.shape[0], y+h), max(0, x-w):max(0, x)]
            right_box = thresh[max(0, y):min(frame.shape[0], y+h), min(frame.shape[1], x+w):min(frame.shape[1], x+2*w)]
            
            motion_left = cv2.countNonZero(left_box) if left_box.size > 0 else 0
            motion_right = cv2.countNonZero(right_box) if right_box.size > 0 else 0
            
            # If a lot of pixels change next to your head, you are waving
            if motion_left > (w * h * 0.15) or motion_right > (w * h * 0.15):
                is_waving = True

    prev_gray = gray
    return (len(faces) > 0), dx, dy, is_waving
