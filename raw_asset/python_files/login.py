from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import time
import json

from raw_asset.python_files import const_agricolatools


class LoginMachine():
    def __init__(self):
        self.have_login = False
    
    def loginWebsiteBGA_IfCannotLoginReturnFalse(self, driver: webdriver.Chrome, username, password, save_login_info=True):
        if self.have_login:
            return True
        
        if save_login_info:
            login_info_dict = {
                const_agricolatools.ConstJsonFile().key_login_info_username: username,
                const_agricolatools.ConstJsonFile().key_login_info_password: password}
            with open(const_agricolatools.ConstJsonFile().name_login_info, 'w') as login_info_file:
                json.dump(login_info_dict, login_info_file)
        
        return self.checkCanLoginOrNot(driver=driver, username=username, password=password)
    
    def checkCanLoginOrNot(self, driver, username, password):
        if driver is None:
            # selenium webdriver setting
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            need_save_driver = False
        else:
            need_save_driver = True
        
        driver.get('https://en.boardgamearena.com/account')
        username_input = driver.find_element(By.ID, 'username_input')
        password_input = driver.find_element(By.ID, 'password_input')
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        
        login_button = driver.find_element(By.ID, 'submit_login_button')
        login_button.send_keys(Keys.ENTER)
        
        try:
            WebDriverWait(driver, 10).until(EC.url_changes('https://en.boardgamearena.com/account'))
        except TimeoutError:
            if not need_save_driver:
                driver.quit()
            return False
        
        website_url = driver.current_url
        if not need_save_driver:
            driver.quit()
        
        if website_url == const_agricolatools.URL_HAVE_LOGIN:
            self.have_login = True
            return True
        else:
            return False


if __name__ == '__main__':
    assert False, 'login.py should not be executed'
