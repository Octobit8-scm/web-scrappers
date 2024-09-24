from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from yelp_logger import setup_logger

# Set up the logger using the custom logger module
logger = setup_logger(log_file='logs/yelp.log')

# Set up the chrome options for headless browsing and user agent
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


main_list = []


# Function to scrape each page
def scrape_pages(base_url, num_pages):
    for page_num in range(num_pages):
        page_url = f"{base_url}&start={page_num * 10}"
        logger.info(f"Scraping page {page_num + 1}... URL: {page_url}")

        try:
            driver.get(page_url)
            # Use WebDriverWait to ensure the page has loaded specific elements
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'css-12ly5yx'))  # Adjust this to match the actual class
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Scrape each business link on the page
            for link in soup.findAll('a', {'class': 'y-css-12ly5yx'}):
                title = link.text.strip()  # Ensure to get the text content properly
                href = link.get('href')

                if href and href.startswith('/biz/'):  # Ensure it's a valid business URL
                    full_url = 'https://www.yelp.com' + href
                    logger.info(f"scraping data for {title}")
                    get_inside_data(full_url, title)  # Pass the full URL and title for further processing

            time.sleep(random.uniform(5, 20))  # Sleep to mimic human behavior
        except Exception as e:
            logger.error(f"Error fetching page {page_num + 1}: {e}")


# Function to get data from the individual business page
def get_inside_data(item_url, title):
    try:
        driver.get(item_url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))  # Wait for the business name
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract business details
        name = title if title else soup.find('h1').text
        phone_number = location = website = rating = review_count = ''

        # Extract website
        website_sibling = soup.find('p', string="Business website")
        if website_sibling:
            website = website_sibling.find_next_sibling().text.strip()

        # Extract phone number
        phone_no_sibling = soup.find('p', string="Phone number")
        if phone_no_sibling:
            phone_number = phone_no_sibling.find_next_sibling().text.strip()

        # Extract address
        address_sibling = soup.find('a', string="Get Directions")
        if address_sibling:
            location = address_sibling.parent.find_next_sibling().text.strip()

        # Extract rating
        rating_tag = soup.find('div', attrs={'aria-label': re.compile('star rating')})
        if rating_tag:
            rating = rating_tag['aria-label']

        # Extract review count
        review_tag = soup.find('span', string=re.compile('reviews'))
        if review_tag:
            review_count = review_tag.text.strip()

        # Append to main list
        main_list.append({
            'Title': name,
            'Website': website,
            'Phone Number': phone_number,
            'Location': location,
            'Rating': rating,
            'Review Count': review_count
        })
    except Exception as e:
        logger.error(f"Error fetching data for {title}: {e}")


if __name__ == '__main__':
    # Get user input for business type and location
    business_type = input("Enter the business type: ")
    location = input("Enter the location: ")

    # Construct search URL
    base_url = f"https://www.yelp.com/search?find_desc={business_type.replace(' ', '%20')}&find_loc={location.replace(' ', '%20')}"

    # Number of pages to scrape
    num_pages = int(input("Enter the number of pages to scrape: "))

    # Start scraping
    scrape_pages(base_url, num_pages)

    # Save to CSV file
    if main_list:
        df = pd.DataFrame(main_list)
        filename = f"{business_type}_{location}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
        print(f"Data saved to {filename}")
    else:
        logger.warning("No data scraped")
        print("No data scraped.")

driver.quit()
