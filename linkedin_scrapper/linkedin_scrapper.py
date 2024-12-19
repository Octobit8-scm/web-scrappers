import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the LinkedIn access token from environment variables
ACCESS_TOKEN = os.getenv("linkedin_access_token")

# Base headers for LinkedIn API requests
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}


# Function to fetch user profile information
def fetch_user_profile():
    url = "https://api.linkedin.com/v2/userinfo"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            profile_data = response.json()

            # Remove the 'sub' field
            if 'sub' in profile_data:
                del profile_data['sub']

            print("User profile Data:")
            print(json.dumps(profile_data, indent=4))

            # Convert the JSON data to a pandas DataFrame
            # Flatten nested JSON structures, if any
            data = pd.json_normalize(profile_data)

            # Save the data to an Excel file
            output_file = "linkedin_user_profile_data.xlsx"
            data.to_excel(output_file, index=False)
            print(f"Data written to Excel file: {output_file}")
        else:
            print(f"Failed to fetch profile: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main function to test the LinkedIn API
if __name__ == "__main__":
    print("Fetching LinkedIn Profile Information...")
    fetch_user_profile()