# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from yellowpages_logger import setup_logger

# Set up the logger using the custom logger module
logger = setup_logger(log_file='logs/yellowpages.log')


# Set up the chrome options for headless browsing and user agent
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Data storage
main_list = []


# Fetch and scrape data from a single page
def get_data(page_url):
    try:
        driver.get(page_url)
        logger.info(f"Fetching data from: {page_url}")

        # wait for page content to load dynamically
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('div', class_='result')

        for item in articles:

            name = item.find('a', class_='business-name').text if item.find('a', class_='business-name') else 'N/A'
            street_address = item.find('div', class_='street-address').text if item.find('div', class_='street-address') else 'N/A'
            locality = item.find('div', class_='locality').text if item.find('div', class_='locality') else 'N/A'
            phone = item.find('div', class_='phones phone primary').text if item.find('div', class_='phones phone primary') else 'N/A'
            website = item.find('a', class_='track-visit-website')['href'] if item.find('a', class_='track-visit-website') else 'N/A'

            business = {'Name': name, 'Street_address': street_address, 'Locality': locality, 'Phone': phone, 'Website': website}
            main_list.append(business)
        logger.info("Successfully scraped data")

    except Exception as e:
        logger.error(f"Failed to scrape {page_url}: {str(e)}")


# scrape multiple pages
def scrape_pages(base_url, num_pages):
    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}&page={page_num}"
        logger.info(f"Scraping page {page_num}...")
        get_data(page_url)
        time.sleep(random.uniform(3,6))


# Main execution
if __name__ == "__main__":
    try:
        # Get user input for business type and location
        business_type = input("Enter the business type: ")
        location = input("Enter the location: ")

        # Construct search URL
        base_url = f"https://www.yellowpages.com/search?search_terms={business_type.replace(' ', '%20')}&geo_location_terms={location.replace(' ', '%20')}"

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

    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}")

    finally:
        # Close the WebDriver
        driver.quit()
        logger.info("WebDriver closed.")
