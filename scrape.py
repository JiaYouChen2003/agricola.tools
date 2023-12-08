from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ScrapeMachine(): 
    def __init__(self):
        self.url_en_front = 'https://en.'

    def getCardListFromBGA(self, url=''):
        if url == '':
            url = input('Enter the URL:')
        url_en_backstartnum = url.find('boardgamearena.com')
        url_en = self.url_en_front + url[url_en_backstartnum:]

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        print('Loading recent data...')
        driver.get(url_en)

        card_board = driver.find_element(By.ID, 'player-boards')
        card_list = card_board.find_elements(By.CLASS_NAME, 'card-title')

        return card_list

if __name__ == '__main__':
    print('scrape.py should not be executed')