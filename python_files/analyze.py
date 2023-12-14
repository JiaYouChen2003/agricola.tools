import const_agricolatools

class AnalyzeMachine():
    def __init__(self):
        bla = True
    
    def getCardRankMean(self, card_info_arr, player_num = 0):
        total_rank = 0
        total_card = 0
        
        if player_num == 0:
            for card_info in card_info_arr:
                if card_info[1] != None:
                    total_rank += card_info[1]
                    total_card += 1
            
            mean = int(total_rank / total_card)
            return mean
        else:
            for card_info in card_info_arr:
                if card_info[1] != None and card_info[3] == player_num:
                    total_rank += card_info[1]
                    total_card += 1
            
            mean = int(total_rank / total_card)
            return mean
