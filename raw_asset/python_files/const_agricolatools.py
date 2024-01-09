import os

# Const that can an be translate
AUTO_REFRESH_LIST = ['off', 'on']

CARD_INFO_LABEL = ["Card Name", "Card Rank", "Card Diff"]
CARD_MEAN_LABEL = 'Mean: '
CARD_PLAYER_LABEL = 'Player: '
CARD_PLAYER_LABEL_ALL = 'All'

GAME_TYPE_LIST = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']

MESSAGE_CANNOT_LOGIN = 'Cannot Login'
MESSAGE_DRAFTPHASE = 'Still in Draft Phase'

QLABEL_AUTO_REFRESH = 'Auto Refresh:'
QLABEL_PASSWORD = 'Password'
QLABEL_RESULT = 'Results:'
QLABEL_URL_1 = 'URL or'
QLABEL_URL_2 = 'Card Name:'
QLABEL_USERNAME = 'Username'

TEXT_CARD_CANNOT_FIND = 'Cannot Found Card :('
TEXT_CARD_SEARCHED = 'Card Searched!'
TEXT_END_AUTO_REFRESH = 'End Auto Refresh'
TEXT_INTERRUPT_AUTO_REFRESH = 'Interrupt Refresh!'
TEXT_SEARCH_BUTTON = 'search'
TEXT_SEARCHING_CARD = 'Searching Card...'
TEXT_SEARCHING_DONE = 'Searching Done!'
TEXT_SEARCHING_WEBSITE = 'Searching Website...'

URL_LANGUAGE_PREFIX = 'https://en.'
URL_REQUIRE_HINT = 'Enter the URL:'

# Following code do not need to translate
class ConstMessage():
    def __init__(self):
        self.draftphase = 'Still in Draft Phase'
        self.cannot_login = 'Cannot Login'
        
        self.all_message = []
        # search for all variable in self
        for const_message_name in dir(self):
            if const_message_name == 'all_message' or const_message_name.startswith('__'):
                continue
            const_message = getattr(self, const_message_name)
            self.all_message.append(const_message)

class Path():
    def __init__(self):
        # Seen as in the same file with main.py
        self.window_icon_path = os.path.abspath('./raw_asset/agricola-en.jpg')
        self.xlsx_path = os.path.abspath('./raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')
        self.xlsx_workbook_diff_name = 'Diff'

class JsonFile():
    def __init__(self):
        self.name_login_info = 'login_info.json'
        self.key_login_info_username = 'username'
        self.key_login_info_password = 'password'