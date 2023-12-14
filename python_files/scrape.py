from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import const_agricolatools

class MessageCard():
    def __init__(self, message):
        self.text = message
        self.size = {'height': 100}

class ScrapeMachine(): 
    def __init__(self):
        self.url_en_front = 'https://en.'
    
    def getCardListFromBGA(self, url=''):
        if url == '':
            url = input(const_agricolatools.URL_REQUIRE_HINT)
        url_en_backstartnum = url.find('boardgamearena.com')
        url_en = self.url_en_front + url[url_en_backstartnum:]
        
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        html = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        html.get(url_en)
        
        main_tile_text = html.find_element(By.XPATH, './/span[@id="pagemaintitletext"]')
        is_draftphase = self.checkDraftPhase(main_title_text=main_tile_text)
        
        # if still in draft phase, return fake card that say still in draft phase
        if is_draftphase:
            card_draftphase_name = const_agricolatools.ConstMessage().draftphase
            card_draftphase = MessageCard(card_draftphase_name)
            return [card_draftphase]
        
        card_board = html.find_element(By.ID, 'player-boards')
        card_list = card_board.find_elements(By.XPATH, './/*[@class="card-title" or @class="player-board-name"]')
        
        return card_list
    
    def checkDraftPhase(self, main_title_text):
        if main_title_text.text[6:12] == 'Draft:':
            return True
        return False

# test from search.py
if __name__ == '__main__':
    assert False, 'scrape.py should not be executed'