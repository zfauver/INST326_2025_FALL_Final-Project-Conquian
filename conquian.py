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

    for m in melds:
        hand_count = sum(1 for c in m if c in hand)
        use_top = top_card in m
        
        score = (hand_count, use_top, len(m))
        best_score = (best_count, top_card in best, len(best))
        
        if score > best_score:
            best = m
            best_count = hand_count
    
    if best_count == 0:
        return([], False)
    return (best, top_card in best)

# Zachary Fauver
##Funtion requires a helper funtion that determines if a card can be melded
def force_meld(self, current_draw):
    """ Determines if the player(self) should force their opponent to take the 
    card (current_draw)
    
    Args:
        current_draw (card): the information about the current card
    Returns
        decision: True if the player decides to force the meld
                    False if the player does not force the meld
        """
    #checks if the card can be melded first, needs to know the current card and
    # the opponents hand
    can_be_forced = self.check_if_meldable(current_draw, self.opponent)

    #if the card cant be melded return false so that the player does not force the meld
    if can_be_forced == False:
        return False
    
    #forcing opponent to meld may help them win by reducing their hand size
    # this function will only force meld if the oponent has a large hand 
    # >=6 cards and if the player's hand is <=4 so that a meld should
    # only be forced when wining 
    
    decision = False #default is not to force the meld unless conditions are right
    if len(self.opponent.hand) >= 8 and len(self.hand) <=4 :
         decision = True
    return decision
    
    
# Amon Bayu
def valid_play(self, available_cards, existing_melds, remaining_cards):
    """
    Checks if card can be played by changing, rearanging, or building new melds
   
    Args:
        avaliable_cards (list): A list of card strings in the player's hand.
        existing_melds (list): A list of melds. Each meld is a list of card strings.
        remaining_cards (list): The card we want to check for playability.
    
    Returns:
        tuple: 
            played_card (str): The card that was played.
            updated_melds (list): The updated list of melds after the play.
    """
    ranks = {}
    for c in available_cards:
        rank = c[:-1]
        if rank not in ranks:
            ranks[rank] = []
        ranks[rank].append(c)
        
        if len (ranks[rank]) == 3:
            new_meld = ranks[rank]
            return (new_meld[0], new_meld + existing_melds)
    suits = {}
    for c in available_cards:
        suit = c[1]
        if suit not in suits:
            suits[suit] = []
        suits[suit].append(c)

        if len(suits[s]) == 3:
            new_meld = suits[s]
            return (new_meld[0], new_meld + existing_melds)
        
    for meld in existing_melds:
        if len(meld) >= 4:
            borrowed_card = meld[0]
            new_meld = [borrowed_card] + available_cards[:2]
            updated_melds = [m for m in existing_melds if m != meld]
            updated_melds.append(new_meld)
            updated_melds.append(meld[1:])
            return (borrowed_card, updated_melds)
        
    return (available_cards[0], existing_melds)
# Sean Liu
def check_if_meldable(current_draw, opposing_player):
    VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'J':8, 'Q':9, 'K':10}
    
    
    #  Loop has two checks:
    #  Is meld a set? Uses the card[0] meaning if a card is "7C", it grabs char 7. Casts meld into a set to remove
    #  duplicates. If the entire set is only length 1, it's a set. 

    #  Is current draw equal to opponent's meld's first card? if so, it is able to be melded.
    
    for meld in opposing_player.melds:
        if len(set(card[0] for card in meld)) == 1:
            if current_draw[0] == meld[0][0]:
                return True
        # If not a set, we check if meld is a sequence instead, if second index of char is C, we check meld's second char
        # Values list conversion required because of A J Q K
        # Equals C? Then we create a values list. We also create a card value var that is the current draw's value
        # Is Card Value a increment or decrement by 1 of values in mend? If so, then it is mendable.
        else:
            if current_draw[1] == meld[0][1]:
                values = sorted([VALUES[card[0]] for card in meld])
                card_val = VALUES[current_draw[0]]
                if card_val == values[0] - 1 or card_val == values[-1] + 1:
                    return True

    return False

