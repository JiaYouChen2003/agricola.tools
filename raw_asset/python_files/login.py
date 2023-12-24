from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

class LoginMachine():
    def loginWebsiteBGA(self, driver, username, password):
        driver.get('https://en.boardgamearena.com/account')
        username_input = driver.find_element(By.ID, 'username_input')
        password_input = driver.find_element(By.ID, 'password_input')
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        
        login_button = driver.find_element(By.ID, 'submit_login_button')
        login_button.send_keys(Keys.ENTER)
        
        time.sleep(5)
    
    def checkCanLogin(self, username, password):
        