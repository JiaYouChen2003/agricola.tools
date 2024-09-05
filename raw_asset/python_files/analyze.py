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
    
    def __getHandLabel(self, hand_card_info_arr):
        hand_label = None
        
        for hand_card_info in hand_card_info_arr:
            card_label = self.__getCardLabel(hand_card_info)
            if card_label is None:
                continue
            
            if hand_label is None:
                hand_label = [[] for _ in range(len(card_label))]
            
            for i in range(len(card_label)):
                if card_label[i] != ['0']:
                    hand_label[i].extend(card_label[i])
        
        return hand_label
    
    def __getCardLabel(self, card_info):
        '''
        return conditions, resources, action space, room
        
        rtype: list(list(str)) | None
        '''
        # ['Card Name', 'early', 'mid', 'late', 'flexible', 'conditional', 'hard commit', 'resources', 'action space', 'room']
        for row in self.synergy_reference:
            if row[0] == card_info[0]:
                return [row[5].split(), row[7].split(), row[8].split(), row[9].split()]
        return None
    
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
                if card_info[1] is not None and card_info[-1] == player_num:
                    total_rank += int(card_info[1])
                    total_card += 1
            
            return int(self.__getMean(total_rank, total_card))
    
    def getCardSynergyScore(self, card_info_arr):
        hand_label = None
        for i, card_info in enumerate(card_info_arr):
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                hand_label = self.__getHandLabel(hand_card_info_arr=card_info_arr[i:])
                break
        
        if hand_label is None:
            return card_info_arr
        
        hand_conditions, hand_resources, hand_action_space, hand_room = hand_label
        for i, card_info in enumerate(card_info_arr):
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                break
            
            card_label = self.__getCardLabel(card_info)
            if card_label is None:
                continue
            
            card_synergy_score = 0
            card_conditions, card_resources, card_action_space, card_room = card_label
            
            for item in hand_conditions:
                if item in card_resources:
                    card_synergy_score += 1
            
            for item in hand_resources:
                if item in card_conditions:
                    card_synergy_score += 1
            
            for item in hand_action_space:
                if item in card_action_space:
                    card_synergy_score += 1
            
            for item in hand_room:
                if item in card_room:
                    card_synergy_score += 1
            
            card_info_arr[i].append(str(card_synergy_score))
            card_info_arr[i][-1], card_info_arr[i][-2] = card_info_arr[i][-2], card_info_arr[i][-1]
        return card_info_arr
