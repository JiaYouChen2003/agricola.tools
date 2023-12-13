import const_agricolatools

class AnalyzeMachine():
    def __init__(self):
        bla = True
    
    def showCardRankMean(self, card_info_arr, player_num = 0):
        total_rank = 0
        total_card = 0
        for card_info in card_info_arr:
            if card_info[1] != None:
                total_rank += card_info[1]
                total_card += 1
        
        mean = total_rank / total_card
        
        return mean