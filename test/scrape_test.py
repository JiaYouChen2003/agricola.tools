import pytest

from raw_asset.python_files import *

import json

URL_TESTING = 'https://boardgamearena.com/archive/replay/220106-1001/?table=232174586&player=91977516&comments=84486938'
URL_DEFAULT = 'https://www.google.com'


@pytest.mark.scrape
def test_MessageCard():
    assert MessageCard('test').text == 'test'
    assert MessageCard().size['height'] > 30


@pytest.mark.scrape
def test_getCardListFromBGA_haveUsernamePassword_cardList():
    const_json_file = ConstJsonFile()
    machine_scrape = ScrapeMachine()
    
    if os.path.isfile(const_json_file.name_login_info):
        with open(const_json_file.name_login_info, 'r') as json_file:
            json_dict = json.load(json_file)
            
            card_list = machine_scrape.getCardListFromBGA(
                URL_TESTING,
                username=json_dict[const_json_file.key_login_info_username],
                password=json_dict[const_json_file.key_login_info_password],
                save_login_info=True)
            
            assert len(card_list) == 20
            assert card_list[0].text == 'Grocer'
            assert card_list[1].text == 'Big Country'
            assert card_list[2].text == 'Childless'
            assert card_list[-3].text == 'Small Greenhouse'
            assert card_list[-2].text == 'Carrot Museum'
            assert card_list[-1].text == 'Master Builder'
            for card in card_list:
                assert card.size['height'] > 30


@pytest.mark.false
@pytest.mark.scrape
def test_getCardListFromBGA_noUsernameNoPassword_needLogin():
    machine_scrape = ScrapeMachine()
    
    card_list = machine_scrape.getCardListFromBGA(
        URL_TESTING, save_login_info=False)
    
    assert card_list[0].text == ConstMessage().need_login
    assert card_list[0].size['height'] > 30


@pytest.mark.false
@pytest.mark.scrape
def test_getCardListFromBGA_haveUsernameNoPassword_needLogin():
    machine_scrape = ScrapeMachine()
    
    card_list = machine_scrape.getCardListFromBGA(
        URL_TESTING, username='username', save_login_info=False)
    
    assert card_list[0].text == ConstMessage().cannot_login
    assert card_list[0].size['height'] > 30


@pytest.mark.false
@pytest.mark.scrape
def test_getCardListFromBGA_noURL_needLogin():
    machine_scrape = ScrapeMachine()
    
    card_list = machine_scrape.getCardListFromBGA(
        save_login_info=False)
    
    assert card_list == 'URL_REQUIRED'


@pytest.mark.scrape
def test_checkDraftPhase():
    machine_scrape = ScrapeMachine()
    
    # selenium webdriver setting
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL_DEFAULT)
    
    draft_phase = machine_scrape.checkDraftPhase(driver=driver)
    
    assert draft_phase is False


@pytest.mark.scrape
def test_checkNeedLogin():
    machine_scrape = ScrapeMachine()
    
    # selenium webdriver setting
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL_DEFAULT)
    
    need_login = machine_scrape.checkNeedLogin(driver=driver)
    
    assert need_login is False
