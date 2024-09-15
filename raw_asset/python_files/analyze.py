import csv

from raw_asset.python_files import const_agricolatools


# Hand ... Card score
DO_NOT_WANT_ANOTHER_HARD_COMMIT_SCORE = -50
HAVE_RESOURCES_FOR_SCORE = 2
DO_NOT_HAVE_RESOURCES_FOR_SCORE = -3
WANT_EARLY_FLEX_SCORE = 4
WANT_RESOURCES_FROM_SCORE = 5
HAVE_SAME_ACTION_SPACE_AS_SCORE = 15
HAVE_SAME_ROOM_STRATEGY_AS_SCORE = 7
HAVE_NOT_SAME_ROOM_STRATEGY_AS_SCORE = -7


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
                hand_label[i].append(card_label[i])
        
        return hand_label
    
    def __getCardLabel(self, card_info):
        '''
        return ['early', 'mid', 'late', 'flexible', 'conditional', 'hard commit', 'resources', 'action space', 'room', 'early flex']
        
        rtype: list(list(str)) | None
        '''
        # ['Card Name', 'early', 'mid', 'late', 'flexible', 'conditional', 'hard commit', 'resources', 'action space', 'room']
        for row in self.synergy_reference:
            if row[0] == card_info[0]:
                row = row[1:]
                card_label = [item.split() for item in row]
                return card_label
        return None
    
    def __getPairSynergyScore(self, card_label, hand_label):
        early, mid, late, flexible, conditions, hard_commit, resources, action_space, room = card_label
        hand_early, hand_mid, hand_late, hand_flexible, hand_conditions, hand_hard_commit, hand_resources, hand_action_space, hand_room = hand_label
        
        card_synergy_score = 0
        
        # hand have resources for card, card is better
        if conditions != ['0']:
            for hand_card_resources in hand_resources:
                for item in hand_card_resources:
                    if item in conditions:
                        card_synergy_score += HAVE_RESOURCES_FOR_SCORE
        
        # hand do not have resources for not flexible card that need resources, card is worse
        if card_synergy_score == 0 and flexible == ['0'] and conditions != ['0']:
            card_synergy_score += DO_NOT_HAVE_RESOURCES_FOR_SCORE
        
        # hard commit in hand, do not want another hard commit, card is worse
        if hard_commit == ['1']:
            for hand_card_hard_commit in hand_hard_commit:
                if hand_card_hard_commit == ['1']:
                    card_synergy_score += DO_NOT_WANT_ANOTHER_HARD_COMMIT_SCORE
        
        # hand do not have early flex, want early flex card, card is better
        if early == ['1'] and flexible == ['1']:
            want_early_flex = True
            for hand_card_early, hand_card_flexible in zip(hand_early, hand_flexible):
                if hand_card_early == ['1'] and hand_card_flexible == ['1']:
                    want_early_flex = False
                    break
            if want_early_flex:
                card_synergy_score += WANT_EARLY_FLEX_SCORE
        
        # hand want resources from card, card is better
        if resources != ['0']:
            for hand_card_conditions in hand_conditions:
                for item in hand_card_conditions:
                    if item in resources:
                        card_synergy_score += WANT_RESOURCES_FROM_SCORE
        
        # hand have the same action space with card, card is better
        if action_space != ['0']:
            for hand_card_action_space in hand_action_space:
                for item in hand_card_action_space:
                    if item in action_space:
                        card_synergy_score += HAVE_SAME_ACTION_SPACE_AS_SCORE
        
        # hand have same room strategy with card, card is better
        # hand have different room strategy with card, card is worse
        if room != ['0']:
            for hand_card_room in hand_room:
                for item in hand_card_room:
                    if item in room:
                        card_synergy_score += HAVE_SAME_ROOM_STRATEGY_AS_SCORE
                    elif room != ['0']:
                        card_synergy_score += HAVE_NOT_SAME_ROOM_STRATEGY_AS_SCORE
        return card_synergy_score
    
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
            card_basic_score = 0
            if card_info_arr[i][1] is not None:
                card_basic_score += round((100 - 100 * (float(card_info_arr[i][1]) / 526)), 2)
            card_info_arr[i].insert(-1, str(card_basic_score))
            
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                hand_label = self.__getHandLabel(hand_card_info_arr=card_info_arr[i:])
                break
        
        if hand_label is None:
            return card_info_arr
        
        for i, card_info in enumerate(card_info_arr):
            if card_info[0] == const_agricolatools.CARD_HAND_LABEL:
                break
            
            card_label = self.__getCardLabel(card_info)
            if card_label is None:
                continue
            
            card_synergy_score = self.__getPairSynergyScore(card_label, hand_label)
            card_info_arr[i][-2] = str(float(card_info_arr[i][-2]) + card_synergy_score)
        return card_info_arr
