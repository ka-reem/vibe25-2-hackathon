import requests
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_person_data(linkedin_url=None):
    """Fetch person data from CrustData API"""
    url = "https://api.crustdata.com/screener/person/enrich"
    
    # Use provided URL or default
    profile_url = linkedin_url or "https://www.linkedin.com/in/abhilashchowdhary/"
    
    params = {
        "linkedin_profile_url": profile_url,
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
    print(f"🔗 Profile: {profile_url}")
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
        return True
        
    else:
        print("Error:", response.status_code, response.text)
        return False

if __name__ == "__main__":
    # Get LinkedIn URL from command line argument if provided
    linkedin_url = sys.argv[1] if len(sys.argv) > 1 else None
    fetch_person_data(linkedin_url)
