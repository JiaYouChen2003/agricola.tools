from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from raw_asset.python_files import const_agricolatools
from raw_asset.python_files import login


class MessageCard():
    def __init__(self, message='', size=100):
        self.text = message
        self.size = {'height': size}


class ScrapeMachine():
    def __init__(self):
        self.machine_login = login.LoginMachine()
        
        self.url_language_front = const_agricolatools.URL_LANGUAGE_PREFIX
        
        # selenium webdriver setting
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def getCardListFromBGA(self, url='', username='', password='', save_login_info=True):
        if username != '' or password != '':
            can_login = self.machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(self.driver, username, password, save_login_info=save_login_info)
        else:
            can_login = True
        
        if not can_login:
            card_cannot_login_name = const_agricolatools.ConstMessage().cannot_login
            card_cannot_login = MessageCard(card_cannot_login_name)
            return [card_cannot_login]
        
        # change language
        if url == '':
            return 'URL_REQUIRED'
        # url_en_backstartnum = url.find('boardgamearena.com')
        # url_en = self.url_language_front + url[url_en_backstartnum:]
        
        # self.driver.get(url_en)
        self.driver.get(url)
        
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except TimeoutError:
            self.driver.refresh()
        
        need_login = self.checkNeedLogin()
        if need_login:
            card_need_login_name = const_agricolatools.ConstMessage().need_login
            card_need_login = MessageCard(card_need_login_name)
            return [card_need_login]
        
        is_draftphase = self.checkDraftPhase()
        if is_draftphase:
            # if still in draft phase and not login, return fake card that say still in draft phase
            if username == '':
                card_draftphase_name = const_agricolatools.ConstMessage().draftphase
                card_draftphase = MessageCard(card_draftphase_name)
                return [card_draftphase]
            # If login, return the card that shown on the draft container
            else:
                card_board = self.driver.find_element(By.ID, 'draft-container')
                card_list = card_board.find_elements(By.CLASS_NAME, 'card-title')
        else:
            card_board = self.driver.find_element(By.ID, 'player-boards')
            card_list = card_board.find_elements(By.XPATH, './/*[@class="card-title" or @class="player-board-name"]')
        
        return card_list
    
    def checkDraftPhase(self, driver=None):
        '''
        Return true if is in draftphase
        type: selenium webdriver
        rtype: bool
        '''
        if driver is None:
            driver = self.driver
        
        if driver.find_elements(By.ID, 'turn-number-tooltipable-1') != []:
            return True
        return False
    
    def checkNeedLogin(self, driver=None):
        '''
        Return true if need login
        type: selenium webdriver
        rtype: bool
        '''
        if driver is None:
            driver = self.driver
        
        Sorry = driver.find_elements(By.ID, 'bga_fatal_error_descr')
        if Sorry != []:
            if Sorry[0].text.startswith('Sorry'):
                return True
        return False


# test from search.py
if __name__ == '__main__':
    # ScrapeMachine().getCardListFromBGA()
    assert False, 'scrape.py should not be executed'
