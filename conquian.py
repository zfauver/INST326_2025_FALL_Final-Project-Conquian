import random
import sys
import argparse

VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'J':8, 'Q':9,'K':10}

class Player: 
    """ Represents a player in the game """
    def __init__(self, hand, melds, name):
        """Initalizes a Player 
        Args:
            hand(list): a list of strings that represent the cards in
                the player's hand
            melds(list): A list of lists, that contains valid melds
            name(str): The name of the player 
            """
        self.hand = hand
        self.melds = melds
        self.name = name
        self.opponent = None

    # Baran Sayan
    def optimal_meld(self, hand, top_card):
        """ Finds the optimal meld for the cpu during the current turn.

        Args:
            hand (list): the current hand of the cpu.
            top_card (str): the available card on the top of the deck.
        Returns:
            tuple: A tuple that contains:
                - list: The best meld as a list of strings, empty list if 
                        there is no valid meld.
                - bool: True if top_card is included in the meld, otherwise
                        False.
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
        # >=6 cards and if the player's hand is <=6 so that a meld should
        # only be forced when winning 
        
        decision = False #default is not to force the meld unless conditions are right
        if len(self.opponent.hand) >= 6 and len(self.hand) <=6 :
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

    def unmelded_cards(self):
        """ Calculates the value of cards that are not melded
        
        Returns:
            int: the sum of all of the unmelded cards in the player's hand
        """
        
        melded_cards = set()
        for meld in self.melds:
            for card in meld:
                melded_cards.add(card)
        unmelded = set(self.hand) - melded_cards
        
        total = 0
        for card in unmelded:
           total += VALUES[card[0]]
        
        return total

    # Sean Liu
    def check_if_meldable(self, current_draw, opposing_player):
        VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'J':8, 'Q':9, 'K':10}

        """
        Checks if the current draw has meldable cards.

        Args:
            current_draw (list): The current draw of cards the user has.
            opposing_player (list): The opposing player's melds. 

        Returns:
            boolean: True if the current draw is either a set or a sequence. False otherwise
        """
        
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

    #Baran Sayan
    def meld_from_hand(self):
        """Identifies possible melds that can be made from the player's current
           hand.

        Returns:
            list[list[str]]: List of melds, each meld is represented as a list
            of strings.
        """
        
        melds = []
        rank = {} # Checks for sets
        
        for c in self.hand:
            if c[0] not in rank:
                rank[c[0]] = []
            rank[c[0]].append(c)
        
        for group in rank.values():
            if len(group) >= 3:
                melds.append(group[:3])
        
        suit = {} # Checks for runs
        
        for c in self.hand:
            if c[1] not in suit:
                suit[c[1]] = []
            suit[c[1]].append(c)
        
        for group in suit.values():
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
        
        return melds    


#game class
class Conquian:
    """ A class that manages the game state and rules of the game"""
    def __init__(self):
        """Initalizes the game, creates the deck, discard pile, 
            players, and stock"""
            
        self.deck = self.create_deck()
        self.discard_pile = []
        self.players = []
        self.stock = []

    def create_deck(self, shuffle=True): #Zach F
        """
        Creates and shuffles the 40 card deck, removing 8, 9, and 10
        
        Returns:
            list: a list of string representing cards
        """
        #40 card deck without 8, 9, 10
        #creates a deck with the following ranks and suits
        ranks = ["A","2","3","4","5","6","7","J","Q","K"]
        suits = ["H","D","C","S"]
        deck = []
        #combines the ranks and suits into one card, like a real card deck
        for s in suits:
            for r in ranks:
                deck.append(r+s)
        if shuffle:
            random.shuffle(deck)
        
        return deck
    
    def deal(self):
        """Deals the initial hands to both players and sets up the stock for
           the game.
           
           Side effects:
              - Creates two player objects with 10 cards each.
              - Assigns the opponents to each Player object.
              - Sets self.players to player1 and cpu.
              - Sets self.stock to the remaining cards.
        """
        player1 = Player(self.deck[:10], [], "player1")
        cpu = Player(self.deck[10:20], [], "cpu")
        player1.opponent = cpu
        cpu.opponent = player1
        self.players = [player1, cpu]
        self.stock = self.deck[20:]
        
    def use_force_meld(self,meldforcer,card): #Zach F
        """ Forces the opponent to meld a card

            Args:
                meldforcer (Player): Player initiating force meld.
                card (str): The card that would be forced into the opponent's
                            meld.
            Side effects:
                - Prints message about forced meld.
                - Removes card from player's hand if meld is successful.
                - May modify opponent's melds by appending the card.
        """
        playerforced = meldforcer.opponent
        melded = False
        
        #iterates through opponent melds to determine
        # where the card can be melded
        for meld in playerforced.melds:
            #using the 0 index we 
            # check if the card fits within a set 
            # (A, 2-7, J,Q, or K)
            if meld[0][0] == card[0]:
                meld.append(card)
                melded = True
                break
            #checks if the card fits into a run with the same suit   
            # and has sequential values
            elif meld[0][1] == card[1]:
                vals = [VALUES[c[0]] for c in meld]
                card_val = VALUES[card[0]]
                
                #determines if the card is in sequence by checkong if
                #the value is 1 above or 1 below
                if card_val == min(vals) - 1 or card_val == max(vals) +1:
                    meld.append(card)
                    #sorts the run
                    meld.sort(key=lambda x: VALUES[x[0]])
                    melded = True
                    break
        if melded:
            print(f"Force meld used:\n"
                      f"{card} was forced into {playerforced.name}'s deck")
            if card in playerforced.hand:
                playerforced.hand.remove(card)
                
                
    def game_state(self):  #Sean Liu
        """Prints the current state of the game. (Each player's hand, melds,
           the stock size, and the discard pile).
        """
        
        for p in self.players:
            print(f"{p.name} hand: {p.hand}")
            print(f"{p.name} melds: {p.melds}")
            print(f"{p.name} unmelded card value: {p.unmelded_cards()}")
        print(f"Discard pile: {self.discard_pile}")
        print(f"Stock remaining: {len(self.stock)}")
    
    def win_condition(self, player): #Zach F
        """ Checks if a player has met the winning conditions
        Args:
            player(Player): The player being checked
        Returns:
            bool: True if the player has exactly 11 cards melded
            """
            
        meld_count = sum(len(m) for m in player.melds)
        return meld_count >= 11
    
    def run(self):
        """Executes the main game loop for Conquian. Alternates turns between
           player1 and cpu, handles drawing from stock pile or discard pile,
           manages discards, checks win condition after every turn, allows for
           melding from the drawn cards or from the player's hand.
           
           Side effects:
              - Updates discard and stock pile.
              - Prints the game progress.
              - Changes the hands and melds of the players.
        """
        parser = argparse.ArgumentParser()
        args = parser.parse_args()
        
        self.deal()
        turn = 0 # 0 is player1, 1 is cpu
        
        while len(self.stock) > 0:
            player = self.players[turn]
            print(f"\n{player.name}'s turn")
            self.game_state()
            
            draw = None
            
            if player.name == "player1": #player1 choice to meld
                if self.discard_pile:
                    print(f"\nTop discard: {self.discard_pile[-1]}")
                    choice = (
                        input("Take a card from stock (s) or discard pile? (d)?"
                              ).strip().lower()
                    ) 
                    if choice == 'd':
                        draw = self.discard_pile.pop()
                        player.hand.append(draw)
                        print(f"You drew {draw} from the discard pile.")
                        play, update = (
                            player.valid_play(player.hand, player.melds, draw)
                        )
                        if play:
                            player.melds = update
                            for c in update[-1]:
                                if c in player.hand:
                                    player.hand.remove(c)
                            print(f"You melded {update[-1]}")
                            if self.win_condition(player):
                                print(f"{player.name} wins!")
                                return
                        else:
                            print("Not a valid meld.")
                            self.discard_pile.append(draw)
                            draw = None
                if draw is None:
                    draw = self.stock.pop(0)
                    player.hand.append(draw)
                    print(f"\nYou drew {draw}")
            else:
                if self.discard_pile:
                    top_discard = self.discard_pile[-1]
                    play, update = (
                       player.valid_play(player.hand, player.melds, top_discard)
                    )
                    if play:
                        draw = self.discard_pile.pop()
                        player.hand.append(draw)
                        print(f"CPU took {draw} from the discard pile.")
                        player.melds = update
                        for c in update[-1]:
                            if c in player.hand:
                                player.hand.remove(c)
                        print(f"CPU melded {update[-1]}")
                        if self.win_condition(player):
                                print(f"{player.name} wins!")
                                return
                    else:
                        draw = self.stock.pop(0)
                        player.hand.append(draw)
                        print(f"CPU drew {draw} from the stock.")
                else:
                    draw = self.stock.pop(0)
                    player.hand.append(draw)
                    print(f"CPU drew {draw} from the stock.")
            
            if draw and draw not in [c for meld in player.melds for c in meld]:
                if player.name == "player1":
                    hand_melds = player.meld_from_hand()    
                    if hand_melds:
                        print(f"\nYou can create melds from your hand: "
                              f"{hand_melds}")
                        meld_hand = (
                            input("Meld from hand? (y/n): ").strip().lower()
                        )
                        if meld_hand == 'y':
                            for meld in hand_melds:
                                print(f"Melding {meld}")
                                player.melds.append(meld)
                                for c in meld:
                                    if c in player.hand:
                                        player.hand.remove(c)
                    play, update = (
                        player.valid_play(player.hand, player.melds, draw)
                    )
                    
                    if play:  
                        choice = input(f"Do you want to meld {draw}? " 
                               f"(y/n)").strip().lower()
                        if choice == "y":
                            player.melds = update
                            for c in update[-1]:
                                if c in player.hand:
                                    player.hand.remove(c)
                            print(f"You melded {update[-1]}")
                            if self.win_condition(player):
                                print(f"{player.name} wins!")
                                return
                        else:
                            if player.opponent.force_meld(draw):
                                print(f"\n{player.opponent.name} "
                                      f"forces you to meld.")
                                self.use_force_meld(player.opponent, draw)
                            else:
                                self.discard_pile.append(draw)
                                print(f"{draw} discarded")
                    else:
                        self.discard_pile.append(draw)
                        print(f"Cannot meld {draw}")
                        
                    if player.hand:
                        while True:
                            discard = (
                                input(f"\nChoose a card to discard from "
                                      f"hand {player.hand}: ").strip().upper()
                            )
                            if discard in player.hand:
                                player.hand.remove(discard)
                                self.discard_pile.append(discard)
                                print(f"{discard} discarded")
                                break
                            else:
                                print("Invalid card")
                else: # CPU
                    hand_melds = player.meld_from_hand()
                    if hand_melds:
                        meld = hand_melds[0]
                        print(f"CPU melded {meld}")
                        if self.win_condition(player):
                                print(f"{player.name} wins!")
                                return
                        player.melds.append(meld)
                        for c in meld:
                            if c in player.hand:
                                player.hand.remove(c)
                    
                    play, update = (
                        player.valid_play(player.hand, player.melds, draw)
                    )
                    
                    if play:
                        player.melds = update
                        for c in update[-1]:
                            if c in player.hand:
                                player.hand.remove(c)
                        print(f"CPU melded {update[-1]}")
                        if self.win_condition(player):
                                print(f"{player.name} wins!")
                                return
                    else:
                        self.discard_pile.append(draw)
                        print(f"CPU discarded {draw}")
                    
                    if player.hand:
                        discard = player.hand.pop(0)
                        self.discard_pile.append(discard)
                        print(f"CPU discarded {discard} from hand")
               
               
            if self.win_condition(player):
                print(f"{player.name} wins!")
                return
            turn = 1 - turn # switch between cpu and player turn

        print("\nStock exhausted. Tie.")
    
if __name__ == "__main__":
    game = Conquian()
    game.run()
    



