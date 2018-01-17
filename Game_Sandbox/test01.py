# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 16:29:18 2018

@author: WangDian
"""

import numpy as np
import itertools
import random
from matplotlib import pyplot as plt

np.random.seed(0)
N_players = 500


D_players = {}
for i in range(0, N_players):
    D_players[i]={}
    D_players[i]['Money'] = 1000
    D_players[i]['Ability'] = int(np.random.randint(1, 11))
    D_players[i]['Lucky'] = 0.5
    D_players[i]['win_times'] = 0
    D_players[i]['lose_times'] = 0
    D_players[i]['game_times'] = 0
    D_players[i]['game_history'] = []

def fight(p1, p2):
    s = D_players[p1]['Ability'] + D_players[p2]['Ability']
    if D_players[p1]['Money']>=10 and D_players[p2]['Money']>=10:
        if float(np.random.rand(1)) <= D_players[p1]['Ability']/s:
            p_win = p1
            p_lose = p2
        else:
            p_win = p2
            p_lose = p1
        
        D_players[p_win]['Money'] += 10
        D_players[p_lose]['Money'] -= 10
        D_players[p_win]['win_times'] += 1
        D_players[p_lose]['lose_times'] += 1
        D_players[p_win]['game_times'] += 1
        D_players[p_lose]['game_times'] += 1
        
        D_players[p_win]['game_history'].append((p_win, p_lose, 'win'))
        D_players[p_lose]['game_history'].append((p_lose, p_win, 'lose'))
        return p_win, p_lose
    else:
        return p1, p2
    
    
def battle():
    player_list = list(D_players.keys())
    battle_list = list(itertools.combinations(player_list, 2))
    random.shuffle(battle_list)
    for (p1, p2) in battle_list:
        p_win, p_lose = fight(p1, p2)
        
for i in range(10):
    battle()



Ability = []
Money = []
for i in D_players.keys():
    Ability.append(D_players[i]['Ability'])
    Money.append(D_players[i]['Money'])

plt.scatter(Ability, Money)







