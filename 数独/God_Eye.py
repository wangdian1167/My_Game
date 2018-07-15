# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 08:44:25 2018

解数独
行列均从 0-8
宫从左至右然后从上至下为 1-9

@author: Administrator
"""

import numpy as np
import time
# 判断行列在第几宫
def get_G(i, j):
    m = i//3 + 1
    n = j//3 + 1
    N_G = (m-1)*3+n
    return N_G

# 获得宫的相应行列数
def G_rc(N_G):
    m = (N_G-1)//3 +1
    n = N_G - (m-1)*3
    i_list = [(m-1)*3, (m-1)*3+1, (m-1)*3+2]
    j_list = [(n-1)*3, (n-1)*3+1, (n-1)*3+2]
    return i_list, j_list

# 获得对应行列可能的数字, s为输入的数独矩阵
def prob_num(sm, i, j):
    L = [1,2,3,4,5,6,7,8,9]
    #去同行
    for k in sm[i]:
        if k != 0:
            try:
                L.remove(k)
            except:
                None
    #去同列
    for k in sm[:, j]:
        if k != 0:
            try:
                L.remove(k)
            except:
                None
    #去同宫
    N_G = get_G(i, j)
    i_list, j_list = G_rc(N_G)
    for m in i_list:
        for n in j_list:
            k = sm[m, n]
            if k != 0:
                try:
                    L.remove(k)
                except:
                    None
    return L

# 将可能性列举出来
def prob_num_all(sm):
    L_prob = []
    for i in range(0,9):
        for j in range(0, 9):
            if sm[i, j] == 0:
                 L= prob_num(sm, i, j) # sm_list[-1]
                 L_prob.append([i, j, L])
    return L_prob

# 判断有无违反规则
def rule_check(sm, prt=False):
    check = True
    # 判断行
    for i in range(0, 9):
        k = 0
        for j in range(0, 9):
            if sm[i, j] != 0:
                k += 1
        set1 = set(sm[i,:])
        try:
            set1.remove(0)
        except:
            None
        if len(set1) != k:
            if prt:
                print('第%d行错误'%(i+1))
            check = False
    # 判断列
    for j in range(0, 9):
        k = 0
        for i in range(0, 9):
            if sm[i, j] != 0:
                k += 1
        set1 = set(sm[:,j])
        try:
            set1.remove(0)
        except:
            None
        if len(set1) != k:
            if prt:
                print('第%d列错误'%(j+1))
            check = False
    # 判断宫
    for N_G in range(1, 10):
        i_list, j_list = G_rc(N_G)
        k = 0
        set1 = set([0])
        for i in i_list:
            for j in j_list:
                if sm[i, j] != 0:
                    k += 1
                    set1.add(sm[i, j])
        try:
            set1.remove(0)
        except:
            None
        if len(set1) != k:
            if prt:
                print('第%d宫错误'%(N_G))
            check = False
    # 判断是否无数可填
    for i in range(0, 9):
        for j in range(0, 9):
            if sm[i, j] == 0:
                if len(prob_num(sm, i, j)) == 0:
                    if prt:
                        print('第%d行%d列无数可填'%(i, j))
                    check = False
    return check
    
    
    
    
    

# 寻找 行列宫 中的唯一数
def prob_num_tri(sm, i, j):
    num = 0
    N_G = get_G(i, j)
    i_list, j_list = G_rc(N_G)
    i_list_rest = i_list.copy()
    j_list_rest = j_list.copy()
    i_list_rest.remove(i)
    j_list_rest.remove(j)
    
    # 行宫
    p = -1 # 判断数，当为1时，则说明该位置是宫内行或列的唯一空值
    for n in j_list_rest:
        if sm[i, n] != 0:
            p += 1
    if p == 1:
        # 锁定同行的宫
        N_G_list = [(N_G-1)//3*3 + 1, (N_G-1)//3*3 + 2, (N_G-1)//3*3 + 3]
        N_G_list.remove(N_G)
        i_list_1, j_list_1 = G_rc(N_G_list[0])
        i_list_2, j_list_2 = G_rc(N_G_list[1])
        
        s0 = set(sm[i, j_list_rest])# 本宫其它值
        s1 = set(sm[i_list_rest[0], j_list_1])# 同行一宫上
        s2 = set(sm[i_list_rest[1], j_list_2])# 同行二宫下
        s12 = s1&s2 - s0 #交集
        try:
            s12.remove(0)
        except: 
            None
        if len(s12) > 0:
            num = list(s12)[0]

        s3 = set(sm[i_list_rest[0], j_list_2])# 同行一宫下
        s4 = set(sm[i_list_rest[1], j_list_1])# 同行二宫上
        s34 = s3&s4 - s0 #交集
        try:
            s34.remove(0)
        except: 
            None
        if len(s34) > 0:
            num = list(s34)[0]

        
    # 列宫
    p = -1 # 判断数，当为1时，则说明该位置是宫内行或列的唯一空值
    for m in i_list_rest:
        if sm[m, j] != 0:
            p += 1
    if p == 1:
        # 锁定同列的宫
        N_G_list = [(N_G-1)%3+1, (N_G-1)%3+4, (N_G-1)%3+7]
        N_G_list.remove(N_G)
        i_list_1, j_list_1 = G_rc(N_G_list[0])
        i_list_2, j_list_2 = G_rc(N_G_list[1])
        
        s0 = set(sm[i_list_rest, j])# 本宫其它值
        s1 = set(sm[i_list_1, j_list_rest[0]])# 同列一宫左
        s2 = set(sm[i_list_2, j_list_rest[1]])# 同列二宫右
        s12 = s1&s2 - s0 #交集
        try:
            s12.remove(0)
        except: 
            None
        if len(s12) > 0:
            num = list(s12)[0]

        s3 = set(sm[i_list_2, j_list_rest[0]])# 同列一宫右
        s4 = set(sm[i_list_1, j_list_rest[1]])# 同列二宫左
        s34 = s3&s4 - s0 #交集
        try:
            s34.remove(0)
        except: 
            None
        if len(s34) > 0:
            num = list(s34)[0]
    return num

# 常规解法综合，并判断是否产生错误
def sol_origin(sm, prt=False):
    err = 0
    sm_p = sm.copy()
    for i in range(0, 9):
        for j in range(0, 9):
            if sm_p[i, j] == 0:
                
                # 行列宫分析
                num = prob_num_tri(sm_p, i, j)
                if num != 0:
                    sm_p[i, j] = num
                    if prt:
                        print('行列宫分析', i, j, num)
                    break
                if not rule_check(sm_p):
                    err = 1
                    break
                
                # 唯一数分析
                L= prob_num(sm_p, i, j)#sm_list[-1]
                if len(L) == 1:
                    sm_p[i, j] = L[0]
                    if prt:
                        print('唯一数分析', i, j, L[0])
                    break
                if not rule_check(sm_p):
                    err = 1
                    break
        if err == 1:
            break
    if rule_check(sm_p, prt=prt):
        return sm_p, err
    else:
        print('常规解法出错')
        err = 1
        return sm,   err
    
# 判断数独是否完成
def complete_check(sm):
    complete = False
    if rule_check(sm):
        if 0 not in sm:
            complete = True
    return complete



# 简单  常规解法即可
#sl_0 = [[6,4,0,  0,3,0,  0,0,7],
#        [5,0,1,  0,7,0,  9,0,0],
#        [0,0,0,  0,0,0,  0,1,0],
#       
#        [0,0,4,  9,0,8,  0,6,0],
#        [0,8,0,  0,0,3,  0,2,0],
#        [0,0,0,  4,0,0,  0,0,0],
#       
#        [4,0,0,  1,5,7,  0,3,0],
#        [2,0,8,  3,0,0,  0,4,0],
#        [7,5,0,  0,0,0,  0,9,6]]

# 困难  需要预测
#sl_0 = [[0,0,0,  0,0,6,  0,0,8],
#        [0,6,0,  0,5,0,  0,2,0],
#        [0,2,0,  0,0,7,  0,6,0],
#       
#        [0,5,1,  0,0,9,  0,3,0],
#        [0,0,3,  0,8,0,  7,0,0],
#        [0,0,0,  7,0,5,  1,0,0],
#       
#        [0,3,8,  6,0,0,  0,0,0],
#        [0,0,0,  5,0,3,  9,8,0],
#        [9,0,5,  8,0,0,  0,0,0]]

# 专家  BOSS级别
#sl_0 = [[0,0,0,  0,0,0,  0,0,0],
#        [0,3,0,  0,0,9,  0,5,0],
#        [0,0,9,  8,2,0,  0,1,3],
#       
#        [1,0,7,  0,9,0,  0,0,0],
#        [3,0,0,  0,0,0,  0,4,5],
#        [0,0,0,  0,0,0,  0,0,6],
#       
#        [0,2,0,  0,7,4,  0,0,0],
#        [0,0,0,  9,0,0,  0,0,0],
#        [0,6,0,  1,0,5,  4,0,0]]

# 地狱1  号称最难数独 （21提示）
sl_0 = [[8,0,0,  0,0,0,  0,0,0],
        [0,0,3,  6,0,0,  0,0,0],
        [0,7,0,  0,9,0,  2,0,0],
       
        [0,5,0,  0,0,7,  0,0,0],
        [0,0,0,  0,4,5,  7,0,0],
        [0,0,0,  1,0,0,  0,3,0],
       
        [0,0,1,  0,0,0,  0,6,8],
        [0,0,8,  5,0,0,  0,1,0],
        [0,9,0,  0,0,0,  4,0,0]]

# 地狱2  仅17提示
sl_0 = [[0,5,0,  6,0,0,  0,0,0],
        [0,0,0,  0,0,0,  7,3,0],
        [0,0,0,  1,0,0,  0,0,0],
       
        [0,0,0,  0,7,0,  8,0,0],
        [0,6,0,  0,0,0,  0,5,0],
        [1,0,0,  0,0,0,  0,0,0],
       
        [7,0,0,  0,4,0,  2,0,0],
        [0,0,4,  0,3,0,  0,0,0],
        [0,0,0,  5,0,0,  0,6,0]]


sl_1 = sl_0.copy()

sm = np.array(sl_0)

time_1 = time.time() #开始计时
# 初步填充数字
for N in range(0, 5):
    print(N)
    sm, err = sol_origin(sm, prt=1) # 常规解法
    if err:
        print('错误')
        break

# 进行预测并填充数字
complete = False
out_time = []  # 用于存储填充后未能解出结果的数独，且该数独当前没有违反规则
L_prob= prob_num_all(sm) #分析可能性
r_L = [1,3,5,7]  # 随机指定四个空值用于填充
for r1 in L_prob[r_L[0]][2]:
    for r2 in L_prob[r_L[1]][2]:
        for r3 in L_prob[r_L[2]][2]:
            for r4 in L_prob[r_L[3]][2]:
                sm_p = sm.copy()
                sm_p[L_prob[r_L[0]][0], L_prob[r_L[0]][1]] = r1
                sm_p[L_prob[r_L[1]][0], L_prob[r_L[1]][1]] = r2
                sm_p[L_prob[r_L[2]][0], L_prob[r_L[2]][1]] = r3
                sm_p[L_prob[r_L[3]][0], L_prob[r_L[3]][1]] = r4
                r_combine = [r1, r2, r3, r4]
                if rule_check(sm_p):
                    print('预测数为:', r_combine)
                    k = 0
                    while(1):
                        k += 1
                        if k%10 == 0:
                            print('k:', k)
                        sm_p, err = sol_origin(sm_p, prt=1) # 常规解法
                        if err:
                            break
                        if complete_check(sm_p):
                            complete = True
                            sm_complete = sm_p.copy()
                            break
                        if k > 30:
                            if rule_check(sm_p, prt=1):
                                out_time.append(sm_p.copy())
                                print('备选方案已添加')
                            else:
                                print('超时')
                            break
                if complete:
                    break
            if complete:
                break
        if complete:
            break
    if complete:
        break

# 第二次添加预测值
# 第一次预测填充四个值后，并不能用常规方法完整解出答案，此时需要再预测四个值（在上一次out_time中）
if complete == False:
    print('第一次预测结束，开始对多项情况继续求解')
    out_time2 = []
    for sm in out_time:
        L_prob= prob_num_all(sm) #分析可能性
        r_L = [1,3,5,7] # 随机指定四个空值用于填充
        for r1 in L_prob[r_L[0]][2]:
            for r2 in L_prob[r_L[1]][2]:
                for r3 in L_prob[r_L[2]][2]:
                    for r4 in L_prob[r_L[3]][2]:
                        sm_p = sm.copy()
                        sm_p[L_prob[r_L[0]][0], L_prob[r_L[0]][1]] = r1
                        sm_p[L_prob[r_L[1]][0], L_prob[r_L[1]][1]] = r2
                        sm_p[L_prob[r_L[2]][0], L_prob[r_L[2]][1]] = r3
                        sm_p[L_prob[r_L[3]][0], L_prob[r_L[3]][1]] = r4
                        r_combine = [r1, r2, r3, r4]
                        if rule_check(sm_p):
                            print('预测数为:', r_combine)
                            k = 0
                            while(1):
                                k += 1
                                if k%10 == 0:
                                    print('k:', k)
                                sm_p, err = sol_origin(sm_p, prt=0) # 常规解法
                                if err:
                                    break
                                if complete_check(sm_p):
                                    complete = True
                                    sm_complete = sm_p.copy()
                                    print('-----------------------解出答案-------------------------')
                                    break
                                if k > 30:
                                    if rule_check(sm_p, prt=0):
                                        out_time2.append(sm_p.copy())
                                        print('备选方案已添加')
                                    else:
                                        print('超时')
                                    break
                        if complete:
                            break
                    if complete:
                        break
                if complete:
                    break
            if complete:
                break
        if complete:
            break

# 第三次添加预测值（仅限地狱难度）
if complete == False:
    print('第三次预测开始')
    out_time3 = []
    for sm in out_time2:
        L_prob= prob_num_all(sm) #分析可能性
        r_L = [1,3,5,7] # 随机指定四个空值用于填充
        for r1 in L_prob[r_L[0]][2]:
            for r2 in L_prob[r_L[1]][2]:
                for r3 in L_prob[r_L[2]][2]:
                    for r4 in L_prob[r_L[3]][2]:
                        sm_p = sm.copy()
                        sm_p[L_prob[r_L[0]][0], L_prob[r_L[0]][1]] = r1
                        sm_p[L_prob[r_L[1]][0], L_prob[r_L[1]][1]] = r2
                        sm_p[L_prob[r_L[2]][0], L_prob[r_L[2]][1]] = r3
                        sm_p[L_prob[r_L[3]][0], L_prob[r_L[3]][1]] = r4
                        r_combine = [r1, r2, r3, r4]
                        if rule_check(sm_p):
                            print('预测数为:', r_combine)
                            k = 0
                            while(1):
                                k += 1
                                if k%10 == 0:
                                    print('k:', k)
                                sm_p, err = sol_origin(sm_p, prt=0) # 常规解法
                                if err:
                                    break
                                if complete_check(sm_p):
                                    complete = True
                                    sm_complete = sm_p.copy()
                                    print('-----------------------解出答案-------------------------')
                                    break
                                if k > 30:
                                    if rule_check(sm_p, prt=0):
                                        out_time3.append(sm_p.copy())
                                        print('备选方案已添加')
                                    else:
                                        print('超时')
                                    break
                        if complete:
                            break
                    if complete:
                        break
                if complete:
                    break
            if complete:
                break
        if complete:
            break

# 第四次添加预测值（仅限地狱难度）
if complete == False:
    print('第三次预测开始')
    out_time4 = []
    for sm in out_time3:
        L_prob= prob_num_all(sm) #分析可能性
        r_L = [1,3,5,7,9] # 随机指定四个空值用于填充
        for r1 in L_prob[r_L[0]][2]:
            for r2 in L_prob[r_L[1]][2]:
                for r3 in L_prob[r_L[2]][2]:
                    for r4 in L_prob[r_L[3]][2]:
                        for r5 in L_prob[r_L[4]][2]:
                            sm_p = sm.copy()
                            sm_p[L_prob[r_L[0]][0], L_prob[r_L[0]][1]] = r1
                            sm_p[L_prob[r_L[1]][0], L_prob[r_L[1]][1]] = r2
                            sm_p[L_prob[r_L[2]][0], L_prob[r_L[2]][1]] = r3
                            sm_p[L_prob[r_L[3]][0], L_prob[r_L[3]][1]] = r4
                            sm_p[L_prob[r_L[3]][0], L_prob[r_L[3]][1]] = r5
                            r_combine = [r1, r2, r3, r4, r5]
                            if rule_check(sm_p):
                                print('预测数为:', r_combine)
                                k = 0
                                while(1):
                                    k += 1
                                    if k%10 == 0:
                                        print('k:', k)
                                    sm_p, err = sol_origin(sm_p, prt=0) # 常规解法
                                    if err:
                                        break
                                    if complete_check(sm_p):
                                        complete = True
                                        sm_complete = sm_p.copy()
                                        print('-----------------------解出答案-------------------------')
                                        break
                                    if k > 30:
                                        if rule_check(sm_p, prt=0):
                                            out_time4.append(sm_p.copy())
                                            print('备选方案已添加')
                                        else:
                                            print('超时')
                                        break
                            if complete:
                                break
                        if complete:
                            break
                    if complete:
                        break
                if complete:
                    break
            if complete:
                break
        if complete:
            break

if complete:
    print('最终结果为：')
    print(sm_complete)
else:
    print('还没结束！！！')

time_2 = time.time() #结束计时
time_use = (time_2 - time_1)/60
print('最终用时为%3.2f分'%time_use)





















