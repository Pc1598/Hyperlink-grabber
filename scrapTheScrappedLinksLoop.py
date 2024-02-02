from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import requests

def get_all_hyperlinks(url, driver, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    hyperlinks = []

    if not url.startswith(('http://', 'https://')):
        return hyperlinks

    try:
        # Open the URL in the existing Firefox driver
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
            if full_url not in visited_urls:
                hyperlinks.append({'url': full_url})
                visited_urls.add(full_url)
                hyperlinks += get_all_hyperlinks(full_url, driver, visited_urls)

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

    return hyperlinks

# Example usage:
if __name__ == "__main__":
    website_url = input("Enter website URL: ")

    # Configure Firefox options for headless mode
    firefox_options = Options()
    firefox_options.headless = True

    # Initialize Firefox driver
    driver = webdriver.Firefox(options=firefox_options)

    try:
        hyperlinks = get_all_hyperlinks(website_url, driver)

        # Remove duplicate URLs by converting the list of dictionaries to a set of tuples and back to a list of dictionaries
        hyperlinks = [dict(t) for t in {tuple(d.items()) for d in hyperlinks}]

        # Write the hyperlinks to a JSON file
        with open('hyperlinks.json', 'w') as json_file:
            json.dump(hyperlinks, json_file, indent=4)

        print("Hyperlinks saved to hyperlinks.json")

    finally:
        # Close the driver
        driver.quit()
