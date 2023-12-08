from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

url_en_front = 'https://en.'

url = input('Enter the URL:')
url_en_backstartnum = url.find('boardgamearena.com')
url_en = url_en_front + url[url_en_backstartnum:]

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url_en)

card_board = driver.find_element(By.ID, 'player-boards')
card_list = card_board.find_elements(By.CLASS_NAME, 'card-title')

for card in card_list:
    print(card.text)