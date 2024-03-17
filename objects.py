from gpiozero import AngularServo
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

class Drone:
    def __init__ (self, iha):
        self.iha = iha
        self.comma = iha.commands
        self.fire_location = {"x": 0.0, "y": 0.0, "deg": 0.0, "distance": 0.0}
        
        self.fire_detected = False
        self.reset()

    def reset(self):
        self.fire_detected = False
        self.fire_location = {"x": 0.0, "y": 0.0, "deg": 0.0, "distance": 0.0}

    def takeoff(self, alt):
        while self.iha.is_armable is not True:
            print("IHA ARM edilebilir değil...")
            time.sleep(1)
        print("IHA ARM edilebilir durumda")

        self.iha.mode = VehicleMode("GUIDED")
        
        self.iha.armed = True

        while self.iha.armed is not True:
            print("IHA ARM ediliyor...")
            time.sleep(1)
        print("IHA ARM edildi")
        self.iha.simple_takeoff(alt)
        while self.iha.location.global_relative_frame.alt <= alt*0.95:
            print('IHA yüksekligi: ', self.iha.location.global_relative_frame.alt)
            time.sleep(1)
        print(f"IHA {alt} yüksekliğine ulasti")
    
    def mode_change(self, mode: str):
        self.iha.mode = VehicleMode(mode)
        while self.iha.mode != mode:
            print("Mod degisimi bekleniyor...")
            time.sleep(1)
        print(f"IHA {mode} moduna alindi")
    
    def go_vertical(self, alt):
        self.iha.simple_goto(LocationGlobalRelative(self.iha.location.global_relative_frame.lat, self.iha.location.global_relative_frame.lon, alt))
        while abs(self.iha.location.global_relative_frame.alt - alt) >= 0.9:
            print('IHA yüksekligi: ', self.iha.location.global_relative_frame.alt)
            time.sleep(1)
        print(f"IHA {alt} yüksekliğine ulasti")

    def drop_bomb(self):
        print("Bomba bırakılıyor...")
        servo = AngularServo(2, min_pulse_width=0.0006, max_pulse_width=0.0023)
        servo.angle = 90

        iha_first_alt = self.iha.location.global_relative_frame.alt
        self.go_vertical(1)

        time.sleep(3)

        servo.angle = -90
        time.sleep(1)
        print("Bomba bırakıldı yukseliyor...")
        self.go_vertical(iha_first_alt)
    
    def go_to(self, location: LocationGlobalRelative):
        self.iha.simple_goto(location)
        while abs(self.iha.location.global_relative_frame.lat - location.lat) >= 0.15 and abs(self.iha.location.global_relative_frame.lon - location.lon) >= 0.15:
            print("Hedefe gidiliyor...")
            time.sleep(1)
        print("Hedefe ulasildi")

    def set_yaw_deg(self, deg):
        rad = (deg * math.pi / 180)
        msg = self.iha.message_factory.send_attitude_target()
        msg.target_system = self.iha.system_id
        msg.target_component = self.iha.component_id
        msg.type_mask = 0b10000000 
        msg.yaw_angle = deg * math.pi / 180
        self.iha.send_message(msg)
        while abs(self.iha.attitude.yaw - rad) > 1:
            print("Yaw açısı ayarlanıyor...")
            time.sleep(1)
        print(f"Yaw açısı {rad} radyan degerine ayarlandı.")


    def gorev(self):
        print("Alev tespit edildi")
        self.iha.mod_degis("GUIDED")
        alev_deg = self.fire_location["deg"]
        alev_dist = self.fire_location["distance"]

        current_alt = self.iha.location.global_relative_frame.alt

        self.set_yaw_deg(alev_deg)

        alev_pos = LocationGlobalRelative(0, alev_dist, current_alt)
        self.go_to(alev_pos)

        self.drop_bomb()
        self.go_vertical(current_alt)
        self.mode_change("RTL")
