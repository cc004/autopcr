import uuid

def create_quest_token(): 
    return create_battle_start_token()
    # return f'{random.randint(0, 1<<64):16x}'

def create_battle_start_token():
    unique_id = uuid.uuid4()
    token = unique_id.hex[:16]
    return token
