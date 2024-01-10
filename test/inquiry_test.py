import pytest

from raw_asset.python_files import *

URL_TESTING = 'https://boardgamearena.com/archive/replay/220106-1001/?table=232174586&player=91977516&comments=84486938'
CARD_NAME_TESTING = 'Seducer'

@pytest.mark.url
def test_inquiryByUrl_noUsernameNoPassword_needLogin():
    machine_inquiry = InquiryMachine()
    card_info_arr = machine_inquiry.inquiryByUrl(URL_TESTING)
    
    assert card_info_arr[0][0] == ConstMessage().need_login

@pytest.mark.url
def test_inquiryByUrl_haveUsernameNoPassword_cannotLogin():
    machine_inquiry = InquiryMachine()
    card_info_arr = machine_inquiry.inquiryByUrl(URL_TESTING, username = 'abc')
    
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