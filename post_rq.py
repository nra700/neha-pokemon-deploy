import requests

url = "https://neha-pokemon-deploy.onrender.com/start_battle"
payload = {
    "pokemon_a": "Pikachu" ,
    "pokemon_b": "Bulbasaur"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())
