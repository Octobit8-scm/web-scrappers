# import libraries
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from justdail_logger import setup_logger

# Set up the logger using the custom logger module
logger = setup_logger(log_file='logs/justdial.log')


def get_listing_details(item):
    try:
        # Extract business name
        business_name = item.find('div', {'class': 'resultbox_title_anchor'}).text.strip() if item.find('div', {
            'class': 'resultbox_title_anchor'}) else 'N/A'

        # Extract call number details
        call_button_element = item.find('span', class_='jsx-5a783115a9ece035 callcontent callNowAnchor')
        phone_number = call_button_element.text.strip() if call_button_element else "Not directly available"

        # Extract ratings
        ratings = item.find('div', class_='resultbox_totalrate').text.strip() if item.find('div',
                                                                                           class_='resultbox_totalrate') else 'N/A'

        # Extract rating counts
        rating_number_element = item.find('div', class_='resultbox_countrate')
        rating_text = rating_number_element.text.strip() if rating_number_element else 'N/A'
        rating_count = ''.join(
            filter(str.isdigit, rating_text)) if rating_text != 'N/A' else 'N/A'  # extract only digits

        # Extract address
        address = item.find('div', class_='resultbox_address').text.strip() if item.find('div',
                                                                                         class_='resultbox_address') else 'N/A'

        return {
            'Name': business_name,
            'Phone': phone_number,
            'Rating': ratings,
            'Rating Count': rating_count,
            'Address': address
        }
    except AttributeError:
        logger.error("Attribute error: possible missing element.")
        return None

    except Exception as e:
        logger.error(f"Error while extracting details: {e}")

        return None


def main():
    # User inputs for location and business category
    location = input("Enter the location: ").strip()
    business_category = input("Enter the business category: ").strip()

    if not location or not business_category:
        logger.error("Missing inputs: location or business_category cannot be empty.")
        return

    # Selenium setup
    options = Options()
    options.headless = True

    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Show ChromeDriver and Chrome version
        driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        chrome_version = driver.capabilities['browserVersion']
        print(f"ChromeDriver version: {driver_version}")
        print(f"Chrome version: {chrome_version}")

        # Construct the URL using the user inputs
        url = f'https://www.justdial.com/{location}/{business_category.replace(" ", "-")}'
        logger.info(f"Accessing URL: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'resultbox_textbox'))
            )
        except TimeoutException:
            logger.error("Loading took too much time!")
            return

        records = []
        while True:
            logger.info("Parsing the page source and extracting listings.")
            # Parse BeautifulSoup in the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            listings = soup.find_all('div', class_='resultbox_textbox')

            for item in listings:
                record = get_listing_details(item)
                if record:
                    records.append(record)

            logger.info(f"Processed {len(records)} listings so far.")

            # Scroll down to fetch more results
            logger.info("Scrolling down to load more listings.")
            last_height = driver.execute_script("return document.body.scrollHeight")

            i = 0
            max_scrolls = 30

            while i <= max_scrolls:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new listings to load after scrolling
                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'resultbox_textbox'))
                    )
                except TimeoutException:
                    logger.error("Timeout while waiting for listings to load.")
                    break  # Exit the loop if listings didn't load in time

                # Check if the page height changes
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    logger.info("No more content to load, stopping the scroll.")
                    break

                last_height = new_height
                i += 1

            # Once scrolling is complete, break out of the loop
            break

        # Save the extracted data to a CSV file
        csv_file_name = f'{business_category.replace(" ", "_")}_results_{location.replace(" ", "_")}.csv'
        if records:
            try:
                with open(csv_file_name, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Name', 'Phone', 'Rating', 'Rating Count', 'Address'])
                    for record in records:
                        writer.writerow([record['Name'], record['Phone'], record['Rating'], record['Rating Count'],
                                         record['Address']])
                logger.info(f"Data saved to {csv_file_name}")
            except IOError as e:
                logger.error(f"Failed to save csv file: {e}")
        else:
            logger.info("No records to save.")

    except TimeoutException as e:
        logger.error(f"The process timed out while loading the page: {e}")
    except WebDriverException as e:
        logger.error(f"A WebDriver error occurred: {e}")

    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
