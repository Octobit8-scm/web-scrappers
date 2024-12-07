import requests

# Replace with your LinkedIn App credentials
ACCESS_TOKEN = "your_access_token"

# LinkedIn API base URL
BASE_URL = "https://api.linkedin.com/v2"

# Headers for authorization
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Function to search for profiles interested in DevOps and Cloud
def search_profiles(keywords, location=None):
    query_params = {
        "q": "people",
        "keywords": keywords,
        "location": location,
    }
    response = requests.get(f"{BASE_URL}/search", headers=HEADERS, params=query_params)

    if response.status_code == 200:
        results = response.json()
        for person in results.get('elements', []):
            print(f"Name: {person.get('firstName')} {person.get('lastName')}")
            print(f"Headline: {person.get('headline')}")
            print(f"Profile URL: https://www.linkedin.com/in/{person.get('publicIdentifier')}\n")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Search for people interested in DevOps and Cloud services
search_profiles(keywords="DevOps Cloud Services")
