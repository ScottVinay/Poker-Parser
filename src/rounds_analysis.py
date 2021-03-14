import pandas as pd

def get_winner(hand,names):
    for row in hand:
        if 'collected' in row:
            for n in names:
                if n in row:
                    return n

def get_section(hand):
    for sec in ['River','Turn','Flop']:
        if sec in ' '.join(hand):
            return sec
    return 'Preflop'

def get_round_wins(dfraw, names):
    entries = dfraw['entry'][::-1]

    all_hands = []
    hand = []
    active = 0
    for i,e in enumerate(entries):
        if active and '--' not in e:
            hand.append(e)
        if '-- starting hand' in e:
            starter = i
            active = 1
        if '-- ending hand' in e:
            active = 0
            all_hands.append(hand)
            hand = []

    win_on = pd.DataFrame({
        'Name':names,
        'Preflop':[0]*len(names),
        'Flop':[0]*len(names),
        'Turn':[0]*len(names),
        'River':[0]*len(names),
    })

    win_on = win_on.set_index('Name')

    for h in all_hands:
        winner  = get_winner(h,names)
        section = get_section(h)
        win_on.loc[winner,section] += 1

    win_on = win_on.reset_index(drop=False)
    
    win_on_perc = win_on.copy()[['Preflop','Flop','Turn','River']]
    totals = win_on_perc.sum(axis=1)
    for i in range(len(win_on_perc)):
        win_on_perc.loc[i,:] = 100*win_on_perc.loc[i,:]/totals[i]
    win_on_perc['Name'] = names
    
    return win_on, win_on_perc