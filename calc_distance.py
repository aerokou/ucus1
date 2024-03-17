import math

def yawa_donustur(x, y):
	if x > 0 and y > 0:
		return 90 - (math.atan2(y,x) * 180 / math.pi)
	elif x < 0 and y > 0:
		return 360 - (90 - math.atan2(y,x) * 180 / math.pi)
	elif x < 0 and y < 0:
		return 360 - (90 + (math.atan2(y, x) * 180 / math.pi) - 180)
	elif x > 0 and y < 0:
		return 90 - (math.atan2(y, x) * 180 / math.pi)
	elif x == 0 and y > 0:
		return 0
	elif x == 0 and y < 0:
		return 180
	elif x < 0 and y == 0:
		return 270
	elif x > 0 and y == 0:
		return 90
	return 0

def atesin_konumu_global(y, x, drone_lat, drone_lon, alt):
    # Hedef konum için enlem ve boylam ofsetlerini hesaplayın
    target_lon = drone_lon + x * 0.00001144032
    target_lat = drone_lat + y * 0.00001144032

    return target_lat, target_lon, alt

def atesin_konumu(ekran_orani, pixel_pos, yukseklik):
	ekran_x = ekran_orani[0]
	ekran_y = ekran_orani[1]

	orta_x = ekran_x // 2
	orta_y = ekran_y // 2

	pos_x = pixel_pos[0]
	pos_y = pixel_pos[1]

	coord_x = pos_x - orta_x
	coord_y = orta_y - pos_y

	oran = yukseklik / ekran_y

	sonuc = {"x": 0.0, "y": 0.0, "deg": 0.0, "distance": 0}

	sonuc["x"] = coord_x * oran
	sonuc["y"] = coord_y * oran
	sonuc["distance"] = math.sqrt(coord_x**2 + coord_y**2) * oran
	sonuc["deg"] = yawa_donustur(coord_x, coord_y)

	return sonuc

print(atesin_konumu_global(3, 5, 40.711810, 30.024157, 10))

# ! KAMERA DUZGUN TAKILMALI
# ! sağdaki x
# lat = 30
# lon = 40

# ! 111319.444444
# lat = 0.0000012
# lon = 0.0000343
#  2.9  0.000034320984
# 1     0.00001144032