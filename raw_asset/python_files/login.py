from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

import time

class LoginMachine():
    def loginWebsiteBGA_IfCannotLoginReturnFalse(self, driver: webdriver.Chrome, username, password):
        driver.get('https://en.boardgamearena.com/account')
        username_input = driver.find_element(By.ID, 'username_input')
        password_input = driver.find_element(By.ID, 'password_input')
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        
        login_button = driver.find_element(By.ID, 'submit_login_button')
        login_button.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        have_login = driver.find_elements(By.ID, 'submit_login_button')
        if have_login == None:
            return True
        else:
            return False

if __name__ == '__main__':
    assert False, 'login.py should not be executed'