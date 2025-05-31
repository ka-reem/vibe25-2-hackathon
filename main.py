import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = "https://api.crustdata.com/screener/person/enrich"
params = {
    "linkedin_profile_url": "https://www.linkedin.com/in/abhilashchowdhary/",
    "enrich_real_time": "true"
}

# Get API token from environment variable
api_token = os.getenv('CRUSTDATA_API_TOKEN')
if not api_token:
    raise ValueError("CRUSTDATA_API_TOKEN environment variable is not set")

headers = {
    "authorization": f"Token {api_token}",
    "accept": "application/json"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code, response.text)
