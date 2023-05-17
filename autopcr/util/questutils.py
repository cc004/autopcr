import random

def create_quest_token(): 
    return f'{random.randint(0, 1<<64):16x}'
