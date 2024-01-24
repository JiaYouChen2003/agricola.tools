import pytest

from raw_asset.python_files import *

import json

URL_TESTING = 'https://boardgamearena.com/archive/replay/220106-1001/?table=232174586&player=91977516&comments=84486938'
CARD_LIST_TESTING = [MessageCard('Seducer')]
CARD_LIST_TESTING_WITH_PLAYER = [
    MessageCard('Seducer', 10),
    MessageCard('Seducer')]


@pytest.mark.url
def test_getCardInfoArr_haveUsernamePassword_cardInfoArr():
    const_json_file = ConstJsonFile()
    machine_search = SearchMachine()
    
    if os.path.isfile(const_json_file.name_login_info):
        with open(const_json_file.name_login_info, 'r') as json_file:
            json_dict = json.load(json_file)
            
            card_info_arr = machine_search.getCardInfoArr(
                URL_TESTING,
                username=json_dict[const_json_file.key_login_info_username],
                password=json_dict[const_json_file.key_login_info_password],
                save_login_info=True)
            
            assert len(card_info_arr) == 20
            assert card_info_arr[0][0] == 'Grocer'
            assert card_info_arr[1][0] == 'Big Country'
            assert card_info_arr[2][0] == 'Childless'
            assert card_info_arr[-3][0] == 'Small Greenhouse'
            assert card_info_arr[-2][0] == 'Carrot Museum'
            assert card_info_arr[-1][0] == 'Master Builder'


@pytest.mark.card_name
def test_getCardInfoArrFromCardNameList_cardList_cardInfo():
    machine_search = SearchMachine()
    card_info = machine_search.getCardInfoArrFromCardNameList(CARD_LIST_TESTING)
    
    assert len(card_info) == 1
    assert card_info[0][0] == 'Seducer'
    assert card_info[0][3] == 0


@pytest.mark.card_name
def test_getCardInfoArrFromCardNameList_cardListWithPlayer_cardPlayerLabelAndCardInfo():
    machine_search = SearchMachine()
    card_info = machine_search.getCardInfoArrFromCardNameList(CARD_LIST_TESTING_WITH_PLAYER)
    
    assert len(card_info) == 2
    assert card_info[0][0] == const_agricolatools.CARD_PLAYER_LABEL + 'Seducer'
    assert card_info[0][3] == 1
    assert card_info[1][0] == 'Seducer'
    assert card_info[1][3] == 1
