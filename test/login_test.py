import pytest

from raw_asset.python_files import *

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.mark.login
def test_loginWebsiteBGA_IfCannotLoginReturnFalse_loginInfoJson_True():
    const_json_file = ConstJsonFile()
    machine_login = LoginMachine()
    
    if os.path.isfile(const_json_file.name_login_info):
        # selenium webdriver setting
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        
        with open(const_json_file.name_login_info, 'r') as json_file:
            json_dict = json.load(json_file)
            
            assert machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(
                driver,
                json_dict[const_json_file.key_login_info_username],
                json_dict[const_json_file.key_login_info_password]) is True
            
            assert machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(
                driver, '', '', save_login_info=False) is True


@pytest.mark.false
@pytest.mark.login
def test_loginWebsiteBGA_IfCannotLoginReturnFalse_noPassword_False():
    machine_login = LoginMachine()
    
    # selenium webdriver setting
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    
    assert machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(
        driver, 'username', '', save_login_info=False) is False


@pytest.mark.false
@pytest.mark.login
def test_loginWebsiteBGA_IfCannotLoginReturnFalse_noUsername_False():
    machine_login = LoginMachine()
    
    # selenium webdriver setting
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    
    assert machine_login.loginWebsiteBGA_IfCannotLoginReturnFalse(
        driver, '', 'password', save_login_info=False) is False
