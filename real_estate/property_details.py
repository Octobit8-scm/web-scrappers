import requests
from bs4 import BeautifulSoup

def scrape_real_estate(location, **filters):
    """
    Scrapes real estate property details from a platform based on location and filters.

    Args:
        location (str): The location to search properties in.
        filters (dict): Additional filters like price range, property type, etc.

    Returns:
        list: A list of dictionaries with property details.
    """
    base_url = "https://example-realestate.com"  # Replace with the real URL of the platform
    search_url = f"{base_url}/search"

    # Build query parameters
    params = {"location": location}
    params.update(filters)

    try:
        # Send a GET request
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract property details
        properties = []
        listings = soup.find_all("div", class_="property-card")  # Update selector based on the website

        for listing in listings:
            try:
                title = listing.find("h2", class_="property-title").get_text(strip=True)
                price = listing.find("span", class_="property-price").get_text(strip=True)
                address = listing.find("div", class_="property-address").get_text(strip=True)
                details = listing.find("ul", class_="property-details").get_text(separator=", ", strip=True)

                properties.append({
                    "title": title,
                    "price": price,
                    "address": address,
                    "details": details,
                })
            except AttributeError:
                # Skip listings with missing information
                continue

        return properties

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Usage example
if __name__ == "__main__":
    location = "New York"
    filters = {
        "min_price": 500000,
        "max_price": 1000000,
        "property_type": "apartment",
    }

    properties = scrape_real_estate(location, **filters)
    if properties:
        print("Properties found:")
        for property in properties:
            print(property)
    else:
        print("No properties found.")
