# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:24:55 2018

N vs N
按水平分配输赢概率
输赢升降段位

@author: WangDian
"""

import numpy as np
import itertools
import random
from matplotlib import pyplot as plt

# =============================================================================
# 初始化 玩家数据
# =============================================================================
# 设置随机种子
#np.random.seed(0)
#random.seed(0)

# 基本参数
D_players = {} # 玩家字典
N_players = 100 # 玩家数量
Rank_max = 200 # 最高段位

# 设置玩家水平
Ability_init = np.random.randn(N_players)
Ability_int = np.around((np.abs(Ability_init) + 1)**2)
# 设置玩家活跃度


# =============================================================================
# 添加新玩家
# =============================================================================
def add_players(N_players_add):
    for i in range(len(D_players), len(D_players) + N_players_add):
        D_players[i]={}
        D_players[i]['Money'] = 100  # 初始金钱
        
    #    D_players[i]['Ability'] = int(Ability_int[i]) # 玩家水平
        D_players[i]['Ability'] = 2 # 初始玩家水平
        
        D_players[i]['Activity'] = 1 # 活跃度
        D_players[i]['Lucky'] = 0.5 # 幸运值
        
        D_players[i]['win_times'] = 0  # 初始化 胜利次数
        D_players[i]['lose_times'] = 0 # 初始化 失败次数
        D_players[i]['game_times'] = 0 # 初始化 总游戏次数
        D_players[i]['game_history'] = [] # 存储所有游戏历史
        
        D_players[i]['winning_streak'] = 0 # 存储当前连胜信息
        D_players[i]['winning_streak_max'] = 0 # 存储最大连胜信息
        
        D_players[i]['Rank'] = 0 # 存储段位信息

# =============================================================================
# 定义输赢规则
# =============================================================================
def fight(p1, p2):
    if ((D_players[p1]['Money']>=10 and D_players[p2]['Money']>=10) and # 需大于10元才能进入游戏
        (abs(D_players[p1]['Rank'] - D_players[p2]['Rank']) <= 20)): # 两者段位差小于 20 才能匹配
        
        # 玩家水平按 log(Ability) 计算，并分配获胜比例
        s = np.log(D_players[p1]['Ability']) + np.log(D_players[p2]['Ability'])
        if float(np.random.rand(1)) <= np.log(D_players[p1]['Ability'])/s:
            p_win = p1
            p_lose = p2
        else:
            p_win = p2
            p_lose = p1
        
        # =====================================================================
        #  赢家
        # =====================================================================
#        D_players[p_win]['Money'] += 10   # 赢家获利
        D_players[p_win]['win_times'] += 1 # 胜利次数+1
        D_players[p_win]['game_times'] += 1 # 游戏次数+1
        D_players[p_win]['game_history'].append((p_win, p_lose, 'win')) # 添加进游戏历史
        D_players[p_win]['winning_streak'] += 1 #连胜+1
        D_players[p_win]['winning_streak_max'] = max(D_players[p_win]['winning_streak_max'], 
                                                     D_players[p_win]['winning_streak']) #更新最大连胜信息
        
        # 段位
        if D_players[p_win]['winning_streak'] >= 3: #第三连胜开始有连胜奖励
            D_players[p_win]['Rank'] += 2 # 段位增加 连胜奖励
        else:
            D_players[p_win]['Rank'] += 1 # 段位增加
        if D_players[p_win]['Rank'] > Rank_max: # 不能超过最高段位
            D_players[p_win]['Rank'] = Rank_max
        
        # 玩家水平
        D_players[p_win]['Ability'] += 1 # 玩家水平+
        # =====================================================================
        #  输家
        # =====================================================================        
#        D_players[p_lose]['Money'] -= 9   # 输家失利
        D_players[p_lose]['lose_times'] += 1 # 胜利次数+1
        D_players[p_lose]['game_times'] += 1 # 游戏次数+1
        D_players[p_lose]['game_history'].append((p_lose, p_win, 'lose')) # 添加进游戏历史
        D_players[p_lose]['winning_streak_max'] = max(D_players[p_lose]['winning_streak_max'], 
                                                      D_players[p_lose]['winning_streak']) #更新最大连胜信息
        D_players[p_lose]['winning_streak'] = 0 #连胜清零
        
        # 段位
        if D_players[p_lose]['Rank'] > 0: # 段位最低为0
            D_players[p_lose]['Rank'] -= 1 # 段位减少
            
        # 玩家水平
        D_players[p_lose]['Ability'] += 0.2 # 玩家水平+
        return True
    else:
        return False
 
    

# =============================================================================
# 进行游戏
# =============================================================================
def battle():
    global Game_Times
    player_list = list(D_players.keys())
    battle_list = list(itertools.combinations(player_list, 2))
    random.shuffle(battle_list)
    for (p1, p2) in battle_list:
        k = fight(p1, p2)
        Game_Times += k

# =============================================================================
# 开始游戏
# =============================================================================
add_players(N_players)
Game_Times = 0  # 初始化 总游戏次数    
for i in range(15):
    if i < 10:
        add_players(50)  
#    Money = []
#    for i in D_players.keys():
#        Money.append(D_players[i]['Money'])
#    print('总金币：', np.sum(Money))
    
    battle()
    
    Rank = []
    for j in D_players.keys():
        Rank.append(D_players[j]['Rank'])
    print(i+1)
    plt.figure()
    plt.hist(Rank, bins=50)
    plt.show()
    
# =============================================================================
# 统计数据
# =============================================================================
Ability = []
Money = []
Rank = []
winning_streak_max = []
win_times = []
lose_times = []
game_times = []
for i in D_players.keys():
    Ability.append(D_players[i]['Ability'])
    Money.append(D_players[i]['Money'])
    Rank.append(D_players[i]['Rank'])
    winning_streak_max.append(D_players[i]['winning_streak_max'])
    win_times.append(D_players[i]['win_times'])
    lose_times.append(D_players[i]['lose_times'])
    game_times.append(D_players[i]['game_times'])
Players = list(D_players.keys())
#print('最终总金币：', np.sum(Money))
print('总游戏次数：', Game_Times)
# 总矩阵
A = np.concatenate((np.array(Players)[:, np.newaxis], # 0 玩家名
                np.array(Ability)[:, np.newaxis], # 1 玩家水平
                np.array(Money)[:, np.newaxis], # 2 金币
                np.array(Rank)[:, np.newaxis], # 3 段位
                np.array(winning_streak_max)[:, np.newaxis], # 4 最高连胜
                np.array(win_times)[:, np.newaxis], # 5 胜场数
                np.array(lose_times)[:, np.newaxis], # 6 败场数
                np.array(game_times)[:, np.newaxis]), axis = 1) # 7 总游戏次数

# =============================================================================
# 画图
# =============================================================================
#plt.figure()
#plt.hist(A[:, 3], bins=50)
#plt.show()

#A_filted = A[np.where(np.array(A[:, 3])>0)] # 按段位筛选

#plt.figure()
#plt.scatter(Ability, Money)
#plt.show()

#plt.figure()
#plt.hist(A_filted[:, 3], bins=30)
#plt.show()

#plt.scatter(Rank, Money)
win_rate = A[:, 5]/A[:, 7]

plt.figure()
plt.hist(win_rate)
plt.show()

plt.figure()
plt.scatter(A[:, 1], win_rate)
plt.show()

print('游戏次数-水平')
plt.figure()
plt.scatter(A[:, 7], A[:, 1])
plt.show()




















