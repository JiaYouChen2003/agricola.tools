from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urljoin
import sys


def download_images(url, folder='images'):
    # Set up Selenium WebDriver with options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the website
        driver.get(url)
        
        # Get the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        # Close the browser
        driver.quit()
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Find all image tags
    img_tags = soup.find_all('img')
    
    # Download each image
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            # Skip images without a src attribute
            continue
        
        # Make the URL absolute by joining with the base URL
        img_url = urljoin(url, img_url)
        
        # Get the image content
        try:
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            
            # Get the image name
            img_name = os.path.basename(img_url)
            
            # Save the image
            img_path = os.path.join(folder, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_response.content)
            
            print(f"Downloaded {img_url} to {img_path}")
        except requests.RequestException as e:
            print(f"Failed to download {img_url}: {e}")


if __name__ == '__main__':
    download_images(sys.argv[1], sys.argv[2])
