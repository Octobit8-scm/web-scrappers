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
1. User Input:
- The user is prompted to enter a location and a business category (e.g., "Bangalore" and "Banquet Halls").
- The inputs are used to construct the search URL for the Justdial website.

2. Web Scraping Process:
- The script uses Selenium with a headless Chrome browser to interact with the Justdial website.
- It navigates to the constructed URL, waits for the page content to load, and retrieves the business listings.
- Using BeautifulSoup, it parses the page's HTML source to extract key business details:
     - Business name
     - Phone number
     - Rating and rating count
     - Address
 
3. Scrolling to Load More Data:
- Since Justdial listings are dynamically loaded as you scroll, the script scrolls the page repeatedly to load more results.
- The page height is monitored to determine when there is no more content to load.

4. Error Handling:
- The script uses try-except blocks to handle exceptions such as missing elements, timeouts, and WebDriver issues.
- A custom logger is used to log information, warnings, and errors in the process to logs/justdial.log.
