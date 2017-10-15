import cv2

cap = cv2.VideoCapture(0)
hsv = None

punktid = list()


def mouse_callback(event, x, y, flags, params):
    if event == 2:
        punktid.append(hsv[y][x])


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', mouse_callback)
while (True):

    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
h = list()
s = list()
v = list()
for i in range(len(punktid)):
    h.append(punktid[i][0])
    s.append(punktid[i][1])
    v.append(punktid[i][2])
parameetrid = [min(h), min(s), min(v), max(h), max(s), max(v)]
nimi = ""
while nimi == "":
    objekt = input("Kas palli(p), korvi(k) või väljaku(v) parameetrid? ")
    if objekt == "p":
        nimi = "pall.txt"
    elif objekt == "k":
        nimi = "korv.txt"
    elif objekt == "v":
        nimi = "valjak.txt"
    else:
        print("Vale sisestus, proovi uuesti.")
fail = open(nimi, "w")
for i in parameetrid:
    fail.write(str(i) + ",")
fail.close()
