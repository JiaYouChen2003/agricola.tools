import os

# Seen as in the same file with main.py
WINDOW_ICON_PATH = os.path.abspath('./raw_asset/agricola-en.jpg')
WORKBOOK_DIFF_NAME = 'Diff'
XLSXPATH = os.path.abspath('./raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')

CARD_PLAYER_CLASS_NAME = "player-board-name"

# Const that can an be translate
GAME_TYPE_LIST = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']

CARD_INFO_LABEL = ["Card Name", "Card Rank", "Card Diff"]
CARD_PLAYER_LABEL = 'Player: '
URL_REQUIRE_HINT = 'Enter the URL:'

class ConstMessage():
    def __init__(self):
        self.draftphase = 'Still in Draft Phase'