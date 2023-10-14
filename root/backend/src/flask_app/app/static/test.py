import requests

token = "d25e90aaaec3ca166927de6ca664e9fe9a94"
img = open("an image.png.b64", "r").read()

r = requests.post("http://localhost:5000/api/post", json={"location_lat": 1.0, "location_lon": 1.0, "image": img}, headers={"Authorization": "Bearer "+token})

print(r.status_code)

if r.status_code == 200:
	print(r.json())
