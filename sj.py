import objects
from dronekit import LocationGlobalRelative, connect
import cv2
from calc_distance import atesin_konumu, atesin_konumu_global
import os
import time

try:
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
    iha.takeoff(drone.location.global_relative_frame.alt)
    iha.mode_change("AUTO")

    while True:
        ret, img = cap.read()

        video_kaydi.write(img)

        fire = fire_cascade.detectMultiScale(img, 1.2, 5)
        for (x,y,w,h) in fire:
            ates_pos_ekran = [x+w/2, y+h/2]

            fire_location = atesin_konumu(EKRAN, ates_pos_ekran, drone.location.global_relative_frame.alt)
            loc = atesin_konumu_global(fire_location["y"], fire_location["x"], drone.location.global_relative_frame.lat, drone.location.global_relative_frame.lon, drone.location.global_relative_frame.alt)
            iha.fire_location = LocationGlobalRelative(loc[0], loc[1], loc[2])

            iha.fire_detected = True
            break

        if iha.fire_detected:
            iha.gorev()
            cap.release()
            video_kaydi.release()

            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    cap.release()
    video_kaydi.release()

    cv2.destroyAllWindows()


# ! MOD DEGİSİKLİGİ NASIL OLMALI SOR