import requests

token = "610f5e55f6b22c8a353b1b161485a472852c"
img = open("an image.png.b64", "r").read()

r = requests.post("http://localhost:5000/api/post", json={"location_lat": 1.0, "location_lon": 1.0, "image": img}, headers={"Authorization": "Bearer "+token})

print(r.status_code)

if r.status_code == 200:
	print(r.json())
