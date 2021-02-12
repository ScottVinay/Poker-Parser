import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import re
from dateutil.parser import parse as dtparse

def find(s, ch):
    return np.array([i for i, ltr in enumerate(s) if ltr == ch]).astype(int)

def get_names(df):
    names = []
    for irow in range(len(df)):
        s = df.loc[irow,'entry']
        name_starts = find(s,'"')[::2]+1
        name_ends   = find(s,'@')-1
        if len(name_starts)==0: continue
        name = s[name_starts[0]:name_ends[0]]
        if name not in names:
            names.append(name)
    return names

def get_hand_differential(hand, names):
    hand_diff = {n:0 for n in names}
    
    hand_text_all = ' '.join(hand.entry.values)
    indices = [hand[hand.entry.str.lower().str.startswith(x.lower())].index[0] for x in ['Your hand is','Flop:','Turn:','River:'] if x.lower() in hand_text_all.lower()]
    indices.append(hand.index[-1])
    rounds = [hand.loc[indices[i]:indices[i+1]-1] for i in range(len(indices)-1)]
    
    for rnd in rounds:
        round_diff = get_round_differential(rnd, names)
        for n in names:
            hand_diff[n] += round_diff[n]

    for k in hand_diff.keys():
        hand_diff[k] = np.round(hand_diff[k], 2)
    assert sum(hand_diff.values()).round(2)==0
    return hand_diff
        
def get_number(string):
    num = re.findall(r'\d+\.\d*', string)
    assert len(num)==1
    return float(num[0])
        
def get_round_differential(rnd, names):
    betting_signatures = ['calls','checks','bets','posts']
    taking_signatures = ['returned', 'collected']
    
    diff = {n:0 for n in names}
    
    for i,row in rnd.iterrows():
        text = row['entry']
        
        if 'bets' in text or 'posts' in text:
            diff[which_player(text,names)] -= get_number(text)
            
        elif 'calls' in text or 'raises to' in text:
            diff[which_player(text,names)] = 0-get_number(text)
            
        elif 'returned' in text or 'collected' in text:
            diff[which_player(text,names)] += get_number(text)
        
    return diff           

def which_player(entry, names):
    for n in names:
        if n in entry:
            return n
    return None

def apply_rebuys(df, names):
    pass

def get_buyins(dfraw, names):
    out = {}
    dfi = dfraw[::-1]
    for i, row in dfi.iterrows():
        for n in names:
            if n in row['entry'] and 'joined' in row['entry']:
                out[n] = get_number(row['entry'])
        if set(out.keys())==set(names):
            break
    return out

def get_hand_start_time(hand):
    time_ = hand.reset_index().loc[0,'at']
    time_ = ' '.join(time_.split('T'))
    time_ = time_.strip('Z')
    time_ = dtparse(time_)
    return time_

def get_robust_totals(dfraw, names):
    dfi = dfraw[::-1].reset_index(drop=True)
    starts = dfi[dfi.entry.str.contains('-- starting hand')]
    ends   = dfi[dfi.entry.str.contains('-- ending hand')]
    starts = starts[:len(ends)]
    hands = []

    for i in range(len(starts)):
        hands.append(dfi.loc[starts.index[i]:ends.index[i]])

    buyins = get_buyins(dfraw, names)
    totals = pd.DataFrame({n:[buyins[n]] for n in names})
    totals['handid'] = 0
    totals['time']   = 0
    
    start_time = get_hand_start_time(hands[0])

    for i, h in enumerate(hands, 1):
        hand_time = get_hand_start_time(h)
        hand_delm = (hand_time-start_time).total_seconds()/60
        
        diff = get_hand_differential(h, names)

        totals.loc[i, 'handid'] = i
        totals.loc[i, 'time'] = hand_delm

        for n in names:
            totals.loc[i, n] = totals.loc[i-1, n] + diff[n]

    return totals.round(2)

if __name__=='__main__':
    file_number = 0
    datafiles = os.listdir('../data')
    datafiles = ['../data/' + x for x in datafiles]
    #dfraw = pd.read_csv(datafiles[file_number]).reset_index(drop=True)
    dfraw = pd.read_csv('../data/data_03_12_20.csv').reset_index(drop=True)
    
    names = get_names(dfraw)
    totals = get_robust_totals(dfraw, names)

    print(totals.head())