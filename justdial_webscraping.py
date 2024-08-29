from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


def get_listing_details(item):
    try:
        # Extract business name
        business_name = item.find('div', {'class': 'resultbox_title_anchor'}).text.strip() if item.find('div', {
            'class': 'resultbox_title_anchor'}) else 'N/A'

        # Extract call number details
        call_button_element = item.find('span', class_='jsx-d444e6bc48e0e7f1 callcontent callNowAnchor')
        phone_number = call_button_element.text.strip() if call_button_element else "Not directly available"

        # Extract ratings
        ratings = item.find('div', class_='resultbox_totalrate').text.strip() if item.find('div',
                                                                                           class_='resultbox_totalrate') else 'N/A'
        # Extract rating counts
        rating_number_element = item.find('div', class_='resultbox_countrate')
        rating_text = rating_number_element.text.strip() if rating_number_element else 'N/A'
        rating_count = ''.join(filter(str.isdigit, rating_text)) if rating_text != 'N/A' else 'N/A'  # extract only digits

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
    except Exception as e:
        print(f"Error while extracting record: {e}")
        return None


def main():
    # User inputs for location and business category
    location = input("Enter the location: ").strip()
    business_category = input("Enter the business_category: ").strip()

    # Selenium setup
    options = Options()
    options.headless = False  # set headless to true mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # using the user inputs construct the URL
    url = f'https://www.justdial.com/{location}/{business_category.replace(" ", "-")}'
    print(f"Accessing URL: {url}")
    driver.get(url)
    time.sleep(5)  # Allowing to load initial page

    records = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    try:
        while True:
            # parse BeautifulSoup in the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            listings = soup.find_all('div', class_='resultbox_textbox')

            for item in listings:
                record = get_listing_details(item)
                if record:    # append only if a record is extracted successfully
                    records.append(record)

            print(f"Collected {len(records)} listings.")

            # Scroll down to fetch more results
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)   # wait for load the page

            # Check  if somemore listings were loaded
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("No more listings to load.")
                break
            last_height = new_height
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Results save to csv
        csv_file_name = f'{business_category.replace(" ", "_")}_results_{location.replace(" ", "_")}.csv'
        if records:  # verify if any records to save
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Phone', 'Rating', 'Rating Count', 'Address'])
                for record in records:
                    writer.writerow(
                        [record['Name'], record['Phone'], record['Rating'], record['Rating Count'], record['Address']])
            print(f"Data saved to {csv_file_name}")
        else:
            print("No records to save.")

        driver.quit()


if __name__ == "__main__":
    main()
