import numpy as np
import cv2

cap = cv2.VideoCapture(1)
hsv = None

punktid = list()


def mouse_callback(event, x, y, flags, params):
    if event == 2:
        punktid.append(hsv[y][x])


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', mouse_callback)
while (True):

    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
h=list()
s=list()
v=list()
for i in range(len(punktid)):
    h.append(punktid[i][0])
    s.append(punktid[i][1])
    v.append(punktid[i][2])
alumine=[min(h),min(s),min(v)]
ülemine=[max(h),max(s),max(v)]
print(alumine,ülemine)