from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import const_agricolatools
import login

class MessageCard():
    def __init__(self, message):
        self.text = message
        self.size = {'height': 100}

class ScrapeMachine(): 
    def __init__(self):
        self.url_language_front = const_agricolatools.URL_LANGUAGE_PREFIX
    
    def getCardListFromBGA(self, url = '', username = '', password = ''):
        # selenium webdriver setting
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        if username != '' and password != '':
            can_login = login.LoginMachine().loginWebsiteBGA_IfCannotLoginReturnFalse(driver, username, password)
        if not can_login:
            card_cannot_login_name = const_agricolatools.ConstMessage().cannot_login
            card_cannot_login = MessageCard(card_cannot_login_name)
            return [card_cannot_login]
            
        # change language
        if url == '':
            url = input(const_agricolatools.URL_REQUIRE_HINT)
        url_en_backstartnum = url.find('boardgamearena.com')
        url_en = self.url_language_front + url[url_en_backstartnum:]
        
        driver.get(url_en)
        
        # if still in draft phase, return fake card that say still in draft phase
        is_draftphase = self.checkDraftPhase(driver)
        if is_draftphase:
            card_draftphase_name = const_agricolatools.ConstMessage().draftphase
            card_draftphase = MessageCard(card_draftphase_name)
            return [card_draftphase]
        
        card_board = driver.find_element(By.ID, 'player-boards')
        card_list = card_board.find_elements(By.XPATH, './/*[@class="card-title" or @class="player-board-name"]')
        
        return card_list
    
    def checkDraftPhase(self, driver):
        '''
        Return true if is in draftphase
        type: selenium webdriver
        rtype: bool
        '''
        if driver.find_elements(By.ID, 'turn-number-tooltipable-1') != []:
            return True
        return False

# test from search.py
if __name__ == '__main__':
    # ScrapeMachine().getCardListFromBGA()
    assert False, 'scrape.py should not be executed'