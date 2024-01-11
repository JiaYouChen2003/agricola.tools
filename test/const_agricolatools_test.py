import pytest

import json

from raw_asset.python_files import *


@pytest.mark.const_agri
def test_ConstMessage():
    const_message = ConstMessage()
    all_message = const_message.all_message
    
    assert len(all_message) == 3
    assert all_message[0] == const_message.cannot_login
    assert all_message[1] == const_message.draftphase
    assert all_message[2] == const_message.need_login


@pytest.mark.const_agri
def test_ConstPath():
    const_path = ConstPath()
    
    assert os.path.isfile(const_path.window_icon_path)
    assert os.path.isfile(const_path.xlsx_path)


@pytest.mark.const_agri
def test_ConstJsonFile():
    const_json_file = ConstJsonFile()
    
    if os.path.isfile(const_json_file.name_login_info):
        with open(const_json_file.name_login_info, 'r') as json_file:
            json_dict = json.load(json_file)
            assert json_dict[const_json_file.key_login_info_username] is not None
            assert json_dict[const_json_file.key_login_info_password] is not None
