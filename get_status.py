import requests
 
base_url = 'https://neha-pokemon-deploy.onrender.com'
battle_id = 'c9a77d10-5900-4291-9ff5-76580441a5db'


status_url = f'{base_url}/battle_status/{battle_id}'


response = requests.get(status_url)

if response.status_code == 200:
    status = response.json()
    print(f"Battle Status: {status}")
else:
    print(f"Failed to get battle status. HTTP Status Code: {response.status_code}")
