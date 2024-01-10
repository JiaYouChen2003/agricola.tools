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