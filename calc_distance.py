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

def atesin_konumu_global(x, y, drone_x, drone_y):
	# Hedef konum için enlem ve boylam ofsetlerini hesaplayın
	north_offset = 10 * sin(drone_x * pi / 180)
	east_offset = 10 * cos(drone_x * pi / 180)

	# Hedef konumun enlem ve boylamını hesaplayın
	target_lat = drone_x + north_offset
	target_lon = drone_y + east_offset

	# Hedef konumun irtifasını mevcut konumla aynı tutun
	target_alt = current_location.alt

	return target_lat, target_lon, target_alt

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

# ! KAMERA DUZGUN TAKILMALI
