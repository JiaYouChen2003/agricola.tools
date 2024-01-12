import pytest

from raw_asset.python_files import *

import json

URL_TESTING = 'https://boardgamearena.com/archive/replay/220106-1001/?table=232174586&player=91977516&comments=84486938'
CARD_NAME_TESTING = 'Seducer'


@pytest.mark.url
def test_inquiryByUrl_haveUsernamePassword_cardInfoArr():
    const_json_file = ConstJsonFile()
    machine_inquiry = InquiryMachine()
    
    if os.path.isfile(const_json_file.name_login_info):
        with open(const_json_file.name_login_info, 'r') as json_file:
            json_dict = json.load(json_file)
            card_info_arr = machine_inquiry.inquiryByUrl(
                URL_TESTING,
                username=json_dict[const_json_file.key_login_info_username],
                password=json_dict[const_json_file.key_login_info_password],
                save_login_info=False)
            
            assert len(card_info_arr) == 20
            assert card_info_arr[0][0] == 'Grocer'
            assert card_info_arr[1][0] == 'Big Country'
            assert card_info_arr[2][0] == 'Childless'
            assert card_info_arr[-3][0] == 'Small Greenhouse'
            assert card_info_arr[-2][0] == 'Carrot Museum'
            assert card_info_arr[-1][0] == 'Master Builder'


@pytest.mark.url
def test_inquiryByUrl_noUsernameNoPassword_needLogin():
    machine_inquiry = InquiryMachine()
    card_info_arr = machine_inquiry.inquiryByUrl(URL_TESTING, save_login_info=False)
    
    assert card_info_arr[0][0] == ConstMessage().need_login


@pytest.mark.url
def test_inquiryByUrl_haveUsernameNoPassword_cannotLogin():
    machine_inquiry = InquiryMachine()
    card_info_arr = machine_inquiry.inquiryByUrl(URL_TESTING, username='abc', save_login_info=False)
    
    assert card_info_arr[0][0] == ConstMessage().cannot_login


@pytest.mark.card_name
def test_inquiryByCardName_CardNameTesting_CardNameTesting():
    machine_inquiry = InquiryMachine()
    card_info = machine_inquiry.inquiryByCardName(CARD_NAME_TESTING)
    
    assert card_info[0][0] == CARD_NAME_TESTING


@pytest.mark.card_name
def test_inquiryByCardName_allLowerCase_CardNameTesting():
    machine_inquiry = InquiryMachine()
    card_info = machine_inquiry.inquiryByCardName('seducer')
    
    assert card_info[0][0] == CARD_NAME_TESTING


@pytest.mark.card_name
def test_inquiryByCardName_randomUpperCase_CardNameTesting():
    machine_inquiry = InquiryMachine()
    card_info = machine_inquiry.inquiryByCardName('SEdUceR')
    
    assert card_info[0][0] == CARD_NAME_TESTING
