# INST326-Final-Project-Conquian
The card game Conquian in Python


Presentation: 
https://www.canva.com/design/DAG7DD3Jm2s/ycKLf6tUfal2PK3Vc7MzHw/edit?utm_content=DAG7DD3Jm2s&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Explanation of each file:
- conquian.py: the main file for the game
- read.me: Document explaining the project and how the program works.

Running the game:
- Command: python conquian.py
- terminal inputs:
  - y/n for melding a card, if the card is not meldable the game will not let you meld the card (required)
  - the card you would like to meld needs to be inputed (required)


Instructions:
 - Users need to answer prompts with their decisions
      - whether to meld or not
      - whether to take a card from the discard pile or the stock pile
 - Both of the players hands and melds are shown
 - Stock shows the remaining cards, once this hits 0 the game ends at a tie.
 - Discards are shown as a list

Bibliography:
- "Conquian." Bicycle Cards, https://bicyclecards.com/how-to-play/conquian
  - Used to learn the rules of the game and decide what functions need to be implemented in order to make a functioning version of the game
  
Attribution: 

|Method/function|Primary author|Techniques demonstrated|
|---------------|--------------|-----------------------|
| optimal_meld  | Baran Sayan  | Generator expression  |
| meld_from_hand| Baran Sayan  | Sequence unpacking    |
| check_if_meldable| Sean Liu  | List comprehension    |
| create_deck| Zachary Fauver  | optional parameters and/or keyword arguments   |
| use_force_meld| Zachary Fauver  | f-strings containing expressions   |




