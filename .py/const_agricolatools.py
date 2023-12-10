import os

XLSXPATH = os.path.abspath('../raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')
WINDOW_ICON_PATH = os.path.abspath('../raw_asset/agricola-en.jpg')
CARD_INFO_LABEL = ["Card Name", "Card Rank", "Card Diff"]
GAME_TYPE_LIST = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']
WORKBOOK_DIFF_NAME = 'Diff'

class ConstMessage():
    def __init__(self):
        self.draftphase = 'Still in Draft Phase'