import random
import sys
import argparse

VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'J':8, 'Q':9,'K':10}

class Player: 
    def __init__(self, hand, melds, name):
        self.hand = hand
        self.melds = melds
        self.name = name

    # Baran Sayan
    def optimal_meld(self, hand, top_card):
        """ Finds the optimal meld for the cpu during the current turn.

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
    # Amon Bayu
    def valid_play(self, available_cards, existing_melds, cards):
        """
        Checks if card can be played by changing, rearanging, or building new melds
    
        Args:
            avaliable_cards (list): A list of card strings in the player's hand.
            existing_melds (list): A list of melds. Each meld is a list of card strings.
            cards (str): The card we want to check for playability.
        
        Returns:
            tuple: 
                played_card (str): The card that was played.
                updated_melds (list): The updated list of melds after the play.
        """
        

        rank = cards[:-1]
        suit = cards[-1]
        
        same_rank = []
        for c in available_cards:
            if c[:-1] == rank:
                same_rank.append(c)
        if len(same_rank) >= 3:
            new_meld = same_rank[:3]
            updated_melds = existing_melds[:] + [new_meld]
            return (cards, updated_melds)
        
        
        same_suit = []
        for c in available_cards:
            if c[-1] == suit:
                same_suit.append(c)
        if len(same_suit) >= 3:
            same_suit.sort(key=lambda c: VALUES[c[:-1]])
                
            run = [same_suit[0]]
            i = 1
            while i < len(same_suit):
                if VALUES[same_suit[i][:-1]] == VALUES[run[-1][:-1]] + 1:
                    run.append(same_suit[i])
                else:
                    if len(run) >= 3:
                        break
                    run = [same_suit[i]]
                i += 1
            if len(run) >= 3 and cards in run:
                new_meld = run
                updated_melds = existing_melds[:] + [new_meld]
                return (cards, updated_melds)
            
        for meld in existing_melds:
            if all(m[:-1] == rank for m in meld):
                new_meld = meld + [cards]
                updated_melds = existing_melds[:]
                updated_melds.remove(meld)
                updated_melds.append(new_meld)
                return (cards, updated_melds)
        for meld in existing_melds:
            if all(m[-1] == suit for m in meld):
                values = sorted([VALUES[m[:-1]] for m in meld])
                val = VALUES[cards[:-1]]

                if val == values[0] - 1 or val == values[-1] + 1:
                    new_meld = meld + [cards]
                    updated_melds = existing_melds[:]
                    updated_melds.remove(meld)
                    updated_melds.append(new_meld)
                    return (cards, updated_melds)
        return (None, existing_melds)

    # Sean Liu
    def check_if_meldable(self, current_draw, opposing_player):
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


#game class
class Conquian:
    def __init__(self):
        self.deck = self.create_deck()
        self.discard_pile = []
        self.players = []
        self.stock = []

    def create_deck(self): #Zach F
        #40 card deck without 8, 9, 10
        #creates a deck with the following ranks and suits
        ranks = ["A","2","3","4","5","6","7","J","Q","K"]
        suits = ["H","D","C","S"]
        deck = []
        #combines the ranks and suits into one card, like a real card deck
        for s in suits:
            for r in ranks:
                deck.append(r+s)
        random.shuffle(deck)
        return deck
        
        return deck
    
    def deal(self):
        player1 = Player(self.deck[:10], [], "player1")
        cpu = Player(self.deck[10:20], [], "cpu")
        player1.opponent = cpu
        cpu.opponent = player1
        self.players = [player1, cpu]
        self.stock = self.deck[20:]
    
    def game_state(self):
        for p in self.players:
            print(f"{p.name} hand: {p.hand}")
            print(f"{p.name} melds: {p.melds}")
        print(f"Discard pile: {self.discard_pile}")
        print(f"Stock remaining: {len(self.stock)}")
    
    def win_condition(self, player):
        meld_count = sum(len(m) for m in player.melds)
        return meld_count >= 11
    
    def run(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()
        
        self.deal()
        turn = 0 # 0 is player1, 1 is cpu
        
        while len(self.stock) > 0:
            player = self.players[turn]
            print(f"\n{player.name}'s turn")
            self.game_state()
            
            draw = self.stock.pop(0)
            print(f"{player.name} drew {draw}")
            player.hand.append(draw)
            
            if player.name == "player1": #player1 choice to meld
                choice = input(f"Do you want to meld {draw}? " 
                               f"(y/n)").strip().lower()
                if choice == "y":
                    play, update = player.valid_play(player.hand, player.melds,
                                                     draw)
                    if play:
                        player.melds = update
                        for c in update[-1]:
                            if c in player.hand:
                                player.hand.remove(c)
                        print(f"You melded {update[-1]}")
                    else:
                        print("No valid meld found, discarding")
                        self.discard_pile.append(draw)
                        player.hand.remove(draw)
                else:
                    self.discard_pile.append(draw)
                    player.hand.remove(draw)
            
                if player.hand: #player1 discard
                    discard = input(f"Choose a card to discard from your hand "
                                    f"{player.hand}: ").strip().upper()
                    if discard in player.hand:
                        player.hand.remove(discard)
                        self.discard_pile.append(discard)
            
            else: #cpu
                meld, used_top = player.optimal_meld(player.hand, draw)
                if meld:
                    player.melds.append(meld)
                    for c in meld:
                        if c in player.hand:
                            player.hand.remove(c)
                    print(f"CPU melded {meld}")
                else:
                    discard = player.hand.pop(0)
                    self.discard_pile.append(discard)
                    print(f"CPU discarded {discard}")    
            
            if self.win_condition(player):
                print(f"{player.name} wins!")
                return
            turn = 1 - turn # switch between cpu and player turn

        print("Stock exhausted. Tie.")
    
if __name__ == "__main__":
    game = Conquian()
    game.run()
    

