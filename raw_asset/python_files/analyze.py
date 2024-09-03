import csv

from raw_asset.python_files import const_agricolatools


class AnalyzeMachine():
    def __init__(self):
        self.synergy_reference = []
        with open(const_agricolatools.ConstPath().synergy_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                self.synergy_reference.append(row)
    
    def __getMean(self, sum, num):
        if num == 0:
            return 0
        
        mean = sum / num
        return mean
    
    def getCardRankMean(self, card_info_arr, player_num=0):
        '''
        card_info = [card_name, card_rank, card_diff, card_player_num]
        '''
        total_rank = 0
        total_card = 0
        
        if player_num == 0:
            for card_info in card_info_arr:
                if card_info[1] is not None:
                    total_rank += int(card_info[1])
                    total_card += 1
            
            return int(self.__getMean(total_rank, total_card))
            
        else:
            for card_info in card_info_arr:
                if card_info[1] is not None and card_info[3] == player_num:
                    total_rank += int(card_info[1])
                    total_card += 1
            
            return int(self.__getMean(total_rank, total_card))
    
    def getCardSynergyScore(self, card_info_arr):
        hand_label = None
        for i, card_info in enumerate(card_info_arr):
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                hand_label = self.getHandLabel(hand_card_info_arr=card_info_arr[i:])
                break
        
        if hand_label is None:
            return card_info_arr
        
        for card_info in card_info_arr:
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                break
            
            # if card_info
        
        return card_info_arr
    
    def getHandLabel(self, hand_card_info_arr):
        hand_label = []
        
        for hand_card_info in hand_card_info_arr:
            card_label = self.getCardLabel(hand_card_info)
            if card_label is None:
                continue
            
            if len(hand_label) == 0:
                hand_label = [[] for _ in range(len(card_label))]
            
            for i in range(len(card_label)):
                if card_label[i] != ['0']:
                    hand_label[i].extend(card_label[i])
        
        return hand_label
    
    def getCardLabel(self, card_info):
        # ['Card Name', 'early', 'mid', 'late', 'flexible', 'conditional', 'hard commit', 'resources', 'action space', 'room']
        for row in self.synergy_reference:
            if row[0] == card_info[0]:
                # condition, resources, action space, room
                return [row[5].split(), row[7].split(), row[8].split(), row[9].split()]
        return None
