import cv2
import numpy as np
import serial

con = serial.Serial("COM3", baudrate=115200, timeout=0.8, dsrdtr=True)
pall = open("pall.txt", "r").readline().split(",")
korv = open("korv.txt", "r").readline().split(",")
p = []
k = []
for i in range(6):
    p.append(int(pall[i]))
    k.append(int(korv[i]))

cap = cv2.VideoCapture(1)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    P_alumine = np.array([p[0], p[1], p[2] - 20], np.uint8)
    p_ülemine = np.array([p[3], p[4], p[5] + 20], np.uint8)
    k_alumine = np.array([k[0], k[1], k[2]], np.uint8)
    k_ülemine = np.array([k[3], k[4], k[5]], np.uint8)
    p_mask = cv2.inRange(hsv, P_alumine, p_ülemine)
    k_mask = cv2.inRange(hsv, k_alumine, k_ülemine)
    res1 = cv2.bitwise_and(frame, frame, mask=p_mask)
    res2 = cv2.bitwise_and(frame, frame, mask=k_mask)
    cv2.imshow('frame', frame)
    cv2.imshow('res1', res1)
    # cv2.imshow('res2', res2)
    p_cnts = cv2.findContours(p_mask.copy(), cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]
    p_center = None
    if len(p_cnts) == 0:
        con.write(("sd10:10:10:0" + "\n").encode())
    if len(p_cnts) > 0:
        cp = max(p_cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cp)
        Mp = cv2.moments(cp)
        try:
            p_center = (int(Mp["m10"] / Mp["m00"]), int(Mp["m01"] / Mp["m00"]))
            if p_center[0] < 290:
                print("Vasakule")
                con.write(("sd10:10:10:0" + "\n").encode())
            elif p_center[0] > 350:
                print("Paremale")
                con.write(("sd-10:-10:-10:0" + "\n").encode())
            elif p_center[0] in range(290, 350):
                print("Keskel")
                con.write(("sd:-10:10:0:0" + "\n").encode())
        except:
            p_center = None
            # liigub pallini, saab selle kätte
            # prioriteet=1
    # #while prioriteet==1:
    #     k_cnts = cv2.findContours(k_mask.copy(), cv2.RETR_EXTERNAL,
    #                           cv2.CHAIN_APPROX_SIMPLE)[-2]
    #     k_center = None
    #
    #     if len(k_cnts) > 0:
    #         ck = max(k_cnts, key=cv2.contourArea)
    #         ((x, y), radius) = cv2.minEnclosingCircle(ck)
    #         Mk = cv2.moments(ck)
    #         try:
    #             k_center = (int(Mk["m10"] / Mk["m00"]), int(Mk["m01"] / Mk["m00"]))
    #         except:
    #             k_center = None
    #         # pöörab korvi poole, valib vastavalt kaugusele jõu (ilmselt distance= x ja siis
    #         # järgmine eraldi asi,mis käivitub). Kui tehtud siis
    #         # prioriteet=0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()