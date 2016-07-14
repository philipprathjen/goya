from math import cos


def locationFilter(lat, lng, qs):
	for event in qs:
		event_lat = float(event.lat)
		event_lng = float(event.lng)
		print(event_lat, event_lng)
		lng_aux = 113.20*cos(lat)
		diff= (lng_aux**(-1))*20
		if diff < 0:
			diff=diff*(-1)
		print(diff)
		if event_lat > lat+0.16: ##approx 20km
			qs = qs.exclude(id = event.id)
		if event_lat < lat-0.16: ##approx 20km
			qs = qs.exclude(id = event.id)
		if event_lng > lng + diff:
			qs = qs.exclude(id = event.id)
		if event_lng < lng - diff:
			qs = qs.exclude(id = event.id)
	return qs

