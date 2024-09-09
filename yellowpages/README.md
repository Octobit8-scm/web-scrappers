# Yellow Pages Scraper
## Overview
This Python script is designed to scrape business listings from the Yellow Pages website. Using Selenium for browsing and BeautifulSoup for parsing, the script extracts business details such as name, address, and phone number for a specific business type and location provided by the user. The scraped data is saved into a CSV file for later use.

## Features
- Scrapes business details like name, street address, locality, and phone number.
- Can scrape multiple pages dynamically from the Yellow Pages website.
- Stores the scraped data in a structured CSV file.
- Includes robust logging to track the scraping process.

## Setup
### Prerequisites
- Python 3.x
- Selenium
- BeautifulSoup
- pandas
- Webdriver Manager
- Google Chrome installed

## Python Libraries Used
- selenium
- beautifulsoup4
- webdriver_manager
- csv

## Functionality
1. User Inputs: The script prompts the user to input the following:
   - Business type: The type of business you're looking for (e.g., "restaurants", "plumbers", etc.).
   - Location: The location where you want to find businesses (e.g., "New York", "Los Angeles").
   - Number of Pages: The number of pages of business listings to scrape from the Yellow Pages website.

2. Web Scraping:
  - Selenium is used to simulate web browsing in a headless Chrome browser. It automatically opens the Yellow Pages search results and loads the content dynamically.
  - BeautifulSoup is used to parse the page's HTML content and extract relevant business details like:
       - Business Name
       - Street Address
       - Locality (City, State, Zip Code)
       - Phone Number

3. Pagination:
   - The script navigates through multiple result pages based on the user's input. For each page, it dynamically loads the content, extracts data, and then moves on to the next page.

4. Logging:
   - A logger is integrated to keep track of the scraping progress, log any errors, and ensure smooth execution.
   - Logs are stored in a file named logs/yellowpages.log.
  
5. Data Storage:
   - All the scraped data is stored in a list and eventually saved as a CSV file.
   - The file is named based on the business type and location (e.g., restaurants_New_York.csv).
  
## Code Breakdown
1. Setup and Initialization:
   - Selenium WebDriver is used to automate a headless Chrome browser, which simulates browsing the Yellow Pages website.
   - A custom logger is set up to log all the scraping activities in a log file located at logs/yellowpages.log.

2. get_data(page_url) Function:
   - This function takes a page URL as an argument and fetches the business listings from that page.
   - It extracts the business name, street address, locality, and phone number for each listing on the page and stores this information in a list (main_list).
  
3. scrape_pages(base_url, num_pages) Function:
   - This function iterates through the specified number of pages (provided by the user).
   - For each page, it constructs the URL, calls the get_data() function, and then introduces a random delay to avoid getting blocked by the website.
  
4. Main Execution:
   - The user provides the business type, location, and number of pages to scrape.
   - The script constructs the Yellow Pages search URL, starts scraping data, and saves the collected information into a CSV file.

## Output Format
The output CSV file will contain the following columns:
   - Name: The business name.
   - Street Address: The street address of the business.
   - Locality: The city, state, and zip code.
   - Phone: The contact phone number of the business.

## Usage
1. Run the Script:
    - python yellowpages_scraper.py

2. Provide User Inputs:
   - Business type (e.g., "plumbers", "restaurants").
   - Location (e.g., "Los Angeles", "Chicago").
   - Number of pages to scrape.

3. Scraping Process:
   - The script will automatically navigate the Yellow Pages site, scrape the business listings, and save them in a CSV file.

4. CSV Output:
   - The extracted data will be saved in a file named business_type_location.csv, for example, plumbers_Chicago.csv.


