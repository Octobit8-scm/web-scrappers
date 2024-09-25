# Justdial Business Listings Scraper
## Overview
This Python script is a web scraper designed to extract business listings from the Justdial website based on user inputs for location and business category. The script uses Selenium for web interaction and BeautifulSoup for parsing the HTML content to extract details like business names, phone numbers, ratings, and addresses. The extracted data is saved in a CSV file for future reference.

## Features
- Extracts business details like name, phone number, ratings, and address.
- Scrolls through the Justdial webpage to load more listings dynamically.
- Saves data in a CSV file for easy access.
- Implements logging for better tracking and debugging.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup
- Webdriver Manager
- Google Chrome browser installed

## Python Libraries Used
- selenium
- beautifulsoup4
- webdriver_manager
- csv

## Functionality Overview
The main functionality of the script includes:
### 1. User Input:
- The user is prompted to enter a location and a business category (e.g., "Bangalore" and "Banquet Halls").
- The inputs are used to construct the search URL for the Justdial website.

### 2. Web Scraping Process:
- The script uses Selenium with a headless Chrome browser to interact with the Justdial website.
- It navigates to the constructed URL, waits for the page content to load, and retrieves the business listings.
- Using BeautifulSoup, it parses the page's HTML source to extract key business details:
     - Business name
     - Phone number
     - Rating and rating count
     - Address
 
### 3. Scrolling to Load More Data:
- Since Justdial listings are dynamically loaded as you scroll, the script scrolls the page repeatedly to load more results.
- The page height is monitored to determine when there is no more content to load.

### 4. Error Handling:
- The script uses try-except blocks to handle exceptions such as missing elements, timeouts, and WebDriver issues.
- A custom logger is used to log information, warnings, and errors in the process to logs/justdial.log.

### 5. Saving Data to CSV:
- The extracted business details are stored in a CSV file named after the business category and location.
- If no listings are found, no file is generated.

### 6. Phone Number Retrieval Issue:
- Currently, the script attempts to handle phone numbers hidden behind a "Show Number" button. However, this functionality is not working as expected due to issues with the button interaction and page structure changes.

## Known Issues:
### 1) Phone Number Extraction:
 - The "Show Number" functionality on Justdial is currently facing issues. The script is unable to click the button and reveal hidden phone numbers, so in cases where the number is hidden, "Not directly available" is returned.
### 2) Data Limitation:
 - The script is able to reliably extract up to 10 listings per search category in different cities.

## Code Breakdown
- get_listing_details(item):
    - Extracts details like business name, phone number, rating, and address from each listing. It ensures that if any element is missing, it logs the issue and continues the process.

main():
- The main driver function that:
  - Collects user input
  - Initializes the web driver
  - Navigates to the Justdial URL
  - Handles scrolling and pagination to load more listings
  - Extracts the business details for each listing
  - Saves the data to a CSV file
    
## Output
- CSV File:
   - The output is a CSV file containing the scraped business data, which is saved in the following format:
       -  <business_category>_results_<location>.csv
   - Example: If you search for "Banquet Halls" in "Bangalore," the file will be named Banquet_Halls_results_Bangalore.csv.

- Columns in the CSV File: The CSV file includes the following columns:
    - Name: The name of the business.
    - Phone: The contact number or "Not directly available" if it is not found.
    - Rating: The business rating, or "N/A" if it is unavailable.
    - Rating Count: The number of people who rated the business.
    - Address: The address of the business.

## Example Usage
### 1. Run the Script:
   - python justdial_scraper.py

### 2. Provide User Inputs:
    - Enter the location: e.g., Bangalore
    - Enter the business category: e.g., Banquet Halls
      
### 3. Extracted Data:
   - The scraper will fetch and store the business listings in a CSV file located in the same directory as the script.



