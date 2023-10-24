import requests

token = "e0df0631c7b92864db7bceab1c3f5f91f43b"
img = open("an image.png.b64", "r").read()

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
