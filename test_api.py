from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
api_key = os.getenv("API_KEY")


url = "https://api.soccerdataapi.com/head-to-head/"
querystring = {'team_1_id': 4137, 'team_2_id': 4149, 'auth_token': api_key}
headers = {
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json'
}
response = requests.get(url, headers=headers, params=querystring)
try:
    data = response.json()
except Exception as e:
    pass

print(data.get('stats', {}))