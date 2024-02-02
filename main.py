from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

def get_all_hyperlinks(url):
    hyperlinks = []

    try:
        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--window-size=1920,1200")  # Set window size

        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Open the URL in headless Chrome
        driver.get(url)

        # Wait for the page to load completely (you can adjust this time)
        time.sleep(3)

        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all <a> tags which represent hyperlinks
        links = soup.find_all('a', href=True)

        # Extract and store all hyperlinks
        for link in links:
            href = link.get('href')
            # Join the URL if the link is relative
            full_url = urljoin(url, href)
            hyperlinks.append({'url': full_url})

    finally:
        # Close the driver
        driver.quit()

    return hyperlinks

# Example usage:
if __name__ == "__main__":
    website_url = input("Enter website URL: ")
    hyperlinks = get_all_hyperlinks(website_url)

    # Write the hyperlinks to a JSON file
    with open('hyperlinks.json', 'w') as json_file:
        json.dump(hyperlinks, json_file, indent=4)

    print("Hyperlinks saved to hyperlinks.json")
