# Baran Sayan
def optimal_meld(self, hand, top_card):
    """Finds the optimal meld for the cpu during the current turn.

    Args:
        hand (list): the current hand of the cpu.
        top_card (str): the available card on the top of the deck.
    """
    VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'J':8, 'Q':9,
              'K':10}
    
    cards = hand + [top_card]
    melds = []
    
    rank = {}
    for c in cards:
        if c[0] not in rank:
            rank[c[0]] = []
        rank[c[0]].append(c)
    
    for rank_key, group in rank.items():
        if len(group) >= 3:
            melds.append(group[:3])
            if len(group) == 4:
                melds.append(group)
    
    suit = {}
    for c in cards:
        if c[1] not in suit:
            suit[c[1]] = []
        suit[c[1]].append(c)
    for suit_key, group in suit.items():
        group.sort(key=lambda c: VALUES[c[0]])
        
        for i in range(len(group)):
            run = [group[i]]
            for j in range(i+1, len(group)):
                if VALUES[group[j][0]] == VALUES[run[-1][0]] + 1:
                    run.append(group[j])
                else:
                    break
            if len(run) >= 3:
                melds.append(run)
    
    best = []
    best_count = 0
    
    
# Amon Bayu
# Sean Liu

