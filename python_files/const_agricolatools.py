import os

# Seen as in the same file with main.py
WINDOW_ICON_PATH = os.path.abspath('./raw_asset/agricola-en.jpg')
WORKBOOK_DIFF_NAME = 'Diff'
XLSXPATH = os.path.abspath('./raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')

CARD_PLAYER_CLASS_NAME = "player-board-name"

# Const that can an be translate
AUTO_REFRESH_LABEL = 'Auto Refresh:'
AUTO_REFRESH_TEXT = ['off', 'on']
CARD_CANNOT_FIND_TEXT = 'Cannot Found Card :('
CARD_INFO_LABEL = ["Card Name", "Card Rank", "Card Diff"]
CARD_MEAN_LABEL = 'Mean: '
CARD_PLAYER_LABEL = 'Player: '
CARD_PLAYER_LABEL_ALL = 'All'
CARD_SEARCHED_TEXT = 'Card Searched!'
END_AUTO_REFRESH_TEXT = 'End Auto Refresh'
GAME_TYPE_LIST = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']
INTERRUPT_AUTO_REFRESH_TEXT = 'Interrupt Refresh!'
QLABEL_1_1 = 'URL or'
QLABEL_1_2 = 'Card Name:'
QLABEL_2 = 'Results:'
SEARCH_BUTTON_TEXT = 'search'
SEARCHING_CARD_TEXT = 'Searching Card...'
SEARCHING_DONE_TEXT = 'Searching Done!'
SEARCHING_WEBSITE_TEXT = 'Searching Website...'
URL_REQUIRE_HINT = 'Enter the URL:'


class ConstMessage():
    def __init__(self):
        self.draftphase = 'Still in Draft Phase'