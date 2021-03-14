import numpy as np

'A♦ 2♣ K♠ 3♥ 6♣'
'6♥ A♠'

def which(cards):
    rlc = np.arange(len(cards))
    for trial in [
        'royal_flush',
        'straight_flush',
        'full_house',
        'flush',
        'straight',
        'three_of_a_kind',
        'two_pair',
        'pair',
        ]:
        if eval(f'{trial}(cards)'): return trial
    else:
        return high_card(cards)

def royal_flush(cards):
    pass

def straight_flush(cards):
    pass

def full_house(cards):
    pass

def flush(cards):
    pass

def straight(cards):
    pass

def three_of_a_kind(cards):
    pass

def two_pair(cards):
    for i in range(len(cards)):
        for j in range(len(cards)):
            if i!=j and cards[i]==cards[j]:
                pass

def pair(cards):
    return (
        cards[i]==cards[j]
        for i in range(len(cards))
        for j in range(len(cards))
        if i!=j
        )

def high_card(cards):
    pass


