# Justdial Web Scraper

## Overview
This Python script is designed to scrape business listing details from Justdial for a given location and business category. The script utilizes Selenium with BeautifulSoup to extract and process data from the dynamically loaded Justdial page.

## Features:
- Takes user input for the location and business category.
- Uses Selenium WebDriver to navigate the Justdial website.
- Scrapes information such as:
    - Business Name
    - Phone Number (if visible)
    - Ratings
    - Rating Counts
    - Address
- Automatically scrolls through the page to load more results dynamically.
- Saves the extracted data into a CSV file.

## Requirements:
- Python 3.x
- Chrome WebDriver (managed automatically using webdriver_manager)
- Required Python Libraries:
    - selenium
    - bs4 (BeautifulSoup)
    - webdriver_manager
    - csv
    - Custom logger setup (justdial_logger)

 ## How the Code Works:
 ### 1) User Inputs:
   - The user is prompted to enter a location and a business category (e.g., "restaurants" or "hotels").
### 2) WebDriver Initialization:
   - The script initiates a headless Chrome WebDriver session using the webdriver_manager package to handle dynamic loading.
### 3) URL Construction:
   - The Justdial URL is constructed based on the user input.
### 4) Scraping:
   - The script waits for the listings to load and extracts relevant information for each business listing. It uses BeautifulSoup to parse the page source for details like the business name, phone number, ratings, and address.
### 5) Handling Infinite Scrolling: 
  - The script scrolls down the page to load more results dynamically until there are no more listings to load.
### 6) CSV Output: 
  - Extracted data is saved to a CSV file named based on the user input (e.g., restaurants_results_Bangalore.csv).
### 7) Phone Number Retrieval Issue: 
  - Currently, the script attempts to handle phone numbers hidden behind a "Show Number" button. However, this functionality is not working as expected due to issues with the button interaction and page structure changes.

## Known Issues:
### 1) Phone Number Extraction: 
 - The "Show Number" functionality on Justdial is currently facing issues. The script is unable to click the button and reveal hidden phone numbers, so in cases where the number is hidden, "Not directly available" is returned.
### 2) Data Limitation: 
 - The script is able to reliably extract up to 10 listings per search category in different cities.

## Output:
The script generates a CSV file containing the following columns:
- Name: The name of the business.
- Phone: The phone number of the business (if directly available).
- Rating: The rating of the business (if available).
- Rating Count: The number of reviews or ratings.
- Address: The business address.

Example CSV output:

  ![image](https://github.com/user-attachments/assets/235019c0-cee8-40f5-80d9-b3497a853129)


