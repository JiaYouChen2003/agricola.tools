from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
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
        
        driver.get('https://en.boardgamearena.com/account')
        username_input = driver.find_element(By.ID, 'username_input')
        password_input = driver.find_element(By.ID, 'password_input')
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        
        login_button = driver.find_element(By.ID, 'submit_login_button')
        login_button.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        if driver.current_url == const_agricolatools.URL_HAVE_LOGIN:
            self.have_login = True
            return True
        else:
            return False


if __name__ == '__main__':
    assert False, 'login.py should not be executed'
