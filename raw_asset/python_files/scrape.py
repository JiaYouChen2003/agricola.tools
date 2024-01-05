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
        self.machine_login = login.LoginMachine()
        
        self.url_language_front = const_agricolatools.URL_LANGUAGE_PREFIX
        
        # selenium webdriver setting
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    def getCardListFromBGA(self, url = '', username = '', password = ''):
        if username != '' or password != '':
            can_login = self.machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(self.driver, username, password)
        else:
            can_login = True
        
        if not can_login:
            card_cannot_login_name = const_agricolatools.ConstMessage().cannot_login
            card_cannot_login = MessageCard(card_cannot_login_name)
            return [card_cannot_login]
        
        # change language
        if url == '':
            url = input(const_agricolatools.URL_REQUIRE_HINT)
        url_en_backstartnum = url.find('boardgamearena.com')
        url_en = self.url_language_front + url[url_en_backstartnum:]
        
        self.driver.get(url_en)
        
        is_draftphase = self.checkDraftPhase()
        if is_draftphase:
            # if still in draft phase and not login, return fake card that say still in draft phase
            if username == '':
                card_draftphase_name = const_agricolatools.ConstMessage().draftphase
                card_draftphase = MessageCard(card_draftphase_name)
                return [card_draftphase]
            else:
                card_board = self.driver.find_element(By.ID, 'draft-container')
                card_list = card_board.find_elements(By.CLASS_NAME, 'card-title')
        else:
            card_board = self.driver.find_element(By.ID, 'player-boards')
            card_list = card_board.find_elements(By.XPATH, './/*[@class="card-title" or @class="player-board-name"]')
        
        return card_list
    
    def checkDraftPhase(self):
        '''
        Return true if is in draftphase
        type: selenium webdriver
        rtype: bool
        '''
        if self.driver.find_elements(By.ID, 'turn-number-tooltipable-1') != []:
            return True
        return False

# test from search.py
if __name__ == '__main__':
    # ScrapeMachine().getCardListFromBGA()
    assert False, 'scrape.py should not be executed'