import requests

base_url = "http://127.0.0.1:8000"

endpoint = "/users/"

print()


# health check
response = requests.get(base_url + "/health/")
if response.status_code == 200:
    print("health details:", response.json(), "\n")
else:
    print("unhealthu:", response.status_code, "\n")

# create user check
user_data = {"username": "hamed", "password": "1234"}
response = requests.post(base_url + endpoint, json=user_data)

if response.status_code == 200:
    print("User created successfully!")
    print("User details:", response.json())
else:
    print("Failed to create user. Status code:", response.status_code, "\n")

# get user check
response = requests.get(base_url + endpoint + "1/")
if response.status_code == 200:
    print("user got successfully!")
    print("User details:", response.json(), "\n")
else:
    print("Failed to get user. Status code:", response.status_code, "\n")
