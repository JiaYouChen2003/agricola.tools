import const_agricolatools

class AnalyzeMachine():
    def __getMean(self, sum, num):
        if num == 0:
            return 0
        
        mean = sum / num
        return mean
        
    def getCardRankMean(self, card_info_arr, player_num = 0):
        total_rank = 0
        total_card = 0
        
        if player_num == 0:
            for card_info in card_info_arr:
                if card_info[1] != None:
                    total_rank += int(card_info[1])
                    total_card += 1
            
            return int(self.__getMean(total_rank, total_card))
            
        else:
            for card_info in card_info_arr:
                if card_info[1] != None and card_info[3] == player_num:
                    total_rank += int(card_info[1])
                    total_card += 1
            
            return int(self.__getMean(total_rank, total_card))