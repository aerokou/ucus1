import objects
from dronekit import LocationGlobalRelative, connect
import cv2
from calc_distance import atesin_konumu
import os
import time

EKRAN = (640, 480)
VIDEO_ADI = "kaydedilen_video.mp4"
i = 0
while os.path.exists(VIDEO_ADI):
    VIDEO_ADI = "kaydedilen_video" + str(i) + ".mp4"
    i += 1
video_kaydi = cv2.VideoWriter(VIDEO_ADI, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, EKRAN)
fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, EKRAN[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, EKRAN[1])

SERVO_PIN = 17

drone = connect("/dev/ttyACM0", wait_ready=True, baud=115200)
iha = objects.Drone(drone, SERVO_PIN)
iha.mode_change("AUTO")

while iha.fire_detected is False:
    ret, img = cap.read()

    video_kaydi.write(img)

    fire = fire_cascade.detectMultiScale(img, 1.2, 5)
    for (x,y,w,h) in fire:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        ates_pos_ekran = [x+w/2, y+h/2]

        iha.fire_location = atesin_konumu(EKRAN, ates_pos_ekran, drone.location.global_relative_frame.alt)
        atesin_konumu_global(iha.fire_location["x"], iha.fire_location["y"], drone.location.global_relative_frame.lat, drone.location.global_relative_frame.lon)

        iha.fire_detected = True
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_kaydi.release()

cv2.destroyAllWindows()

if iha.fire_detected:
    iha.gorev()

    # ! MOD DEGİSİKLİGİ NASIL OLMALI SOR
