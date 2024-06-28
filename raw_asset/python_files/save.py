import json
import os


def saveCardToJSON(card_name, card_rank, card_diff, new_file=False):
    card_details = {
        'card_name': card_name,
        'card_rank': card_rank,
        'card_diff': card_diff
    }

    file_path = 'json/card_details.json'
    
    if new_file or not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump([card_details], json_file, indent=4)
    else:
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = []
        
        data.append(card_details)
        
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
