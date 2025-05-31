import requests
import os
import json
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

print("🔍 Fetching person data from CrustData API...")
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("✅ Data fetched successfully!")
    
    # Save data to JSON file
    filename = "person_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Data saved to {filename}")
    
    # Show brief summary if data is available
    if data and len(data) > 0:
        person = data[0] if isinstance(data, list) else data
        name = person.get('name', 'Unknown')
        current_title = person.get('current_position_title', 'Unknown')
        current_company = person.get('current_company_name', 'Unknown')
        print(f"👤 Name: {name}")
        print(f"💼 Current Role: {current_title} at {current_company}")
        print(f"📊 Data records: {len(data) if isinstance(data, list) else 1}")
    
    print("\n🎯 Ready for analysis! Run 'python llama_client.py' to analyze this data.")
    
else:
    print("Error:", response.status_code, response.text)
