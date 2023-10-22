import requests

token = "3a961bdf155ee8810cba6538ab4b847609a9"
img = open("anderes bild.jpg.b64", "r").read()

a = input()

if a == "1":
	r = requests.post("http://localhost:5000/api/post", json={"location_lat": 1.0, "location_lon": 1.0, "image": img}, headers={"Authorization": "Bearer "+token})

	print(r.status_code)

	if r.status_code == 200:
		print(r.json())
elif a == "2":
	for i in range(-180, 180, 2):
		r = requests.post("http://localhost:5000/api/post", json={"location_lat": i/1.0, "location_lon": i/1.0, "image": img}, headers={"Authorization": "Bearer "+token})

		print(r.status_code)

		if r.status_code == 200:
			print(r.json())
