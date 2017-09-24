import cv2
import numpy as np
lahti=open("parameetrid.txt","r").readline().split(",")
p=[]
for i in range(6):
    p.append(int(lahti[i]))

cap = cv2.VideoCapture(1)
while True:

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    alumine = np.array([p[0], p[1], p[2]], np.uint8)
    ülemine = np.array([p[3], p[4], p[5]], np.uint8)
    mask = cv2.inRange(hsv, alumine, ülemine)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)
    cv2.imshow('res', res)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(center)
        break
cv2.destroyAllWindows()
