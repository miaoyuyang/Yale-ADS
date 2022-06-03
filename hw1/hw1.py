# Mini-project #6 - Blackjack
# Author: Miaoyu Yang
import random

# initialize some useful global variables
global in_play
in_play = False
global outcome
outcome = " start game"
global player_wins
player_wins = 0
global game_result
game_result = 0
score = 0
global table
table = {}
def table_init():
    global table
    for i in range(4, 22):
        for j in range(2, 12):
            table[i, j] = [0, 0]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
        
    def get_value(self):
        rank = self.rank
        value = VALUES[rank]
        if rank == 'A':
            value += 10
        return value

# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            rank = c.get_rank()
            v = VALUES[rank]
            if rank == 'A': aces = True
            value += v
        if aces and value < 12: value += 10
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck 

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck
    
    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck


#define event handlers for buttons
def deal():
    global outcome, in_play, theDeck, playerhand, househand, score, dealerfacecard, game_result
    if in_play:
        outcome = "House winds by default!"
        game_result = 0
        score -= 1
    else:
        outcome = "Hit or stand?"
        game_result = 0
    in_play = True
    theDeck = Deck()
    theDeck.shuffle()
    #print theDeck
    playerhand = Hand()
    househand = Hand()
    playerhand.add_card(theDeck.deal_card())
    playerhand.add_card(theDeck.deal_card())
    dealerfacecard = theDeck.deal_card()
    househand.add_card(dealerfacecard)
    househand.add_card(theDeck.deal_card())
    # print ("Player", playerhand, "Value:", playerhand.get_value())
    # print ("House",  househand, "Value:", househand.get_value())
    # print (theDeck)

def hit():
    global in_play, score, outcome, game_result
    if in_play:
        playerhand.add_card(theDeck.deal_card())
        val = playerhand.get_value()
        # print ("Player", playerhand, "Value:", val)
        if val > 21: 
            outcome = "You are busted! House wins!"
            game_result = 0
            in_play = False
            score -= 1
            # print (outcome, "Score:", score)
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global score, in_play, outcome, game_result
    if playerhand.get_value() > 21:
        outcome = "You are busted."
        game_result = 0
        return None
    if not in_play:
        outcome = "Game is over."
        return None
    val = househand.get_value()
    while(val < 17):
        househand.add_card(theDeck.deal_card())
        val = househand.get_value()  
        # print ("House:", househand, "Value:", val)
    if (val > 21):
        # print ("House is busted!")
        if playerhand.get_value() > 21:
            outcome = "House is busted, but House wins tie game!"
            game_result = 0
            score -= 1
        else: 
            outcome = "House is busted! Player wins!"
            game_result = 1
            score += 1
    else:
        if (val == playerhand.get_value()):
            outcome = "House wins ties!"
            game_result = 0
            score -= 1
        elif (val > playerhand.get_value()):
            outcome = "House wins!"
            game_result = 0
            score -= 1
        else:
            outcome = "Player wins!"
            game_result = 1
            score += 1
    in_play = False
    # print (outcome, "Score:", score)
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

def check_blackjack():
    global score, in_play, outcome, game_result
    if playerhand.get_value() == 21:
        score += 1
        game_result = 1
        outcome = "Player BlackJack!"
        in_play = False

# remember to review the grading rubric
def hitme(playerhand, dealerfacecard):
    global table
    playerval = playerhand.get_value()
    dealerval = dealerfacecard.get_value()
    hit_score = table[(playerval, dealerval)][0]
    stand_score = table[(playerval, dealerval)][1]
    if hit_score == stand_score:
        result = random.random() > 0.5
    else:
        result = hit_score > stand_score
    return result

def sim(trials):
    global player_wins
    for _ in range(trials):
        deal()
        cases_hit = []
        cases_stand = []
        while(in_play):
            player_val = playerhand.get_value()
            dealer_val = dealerfacecard.get_value()
            if hitme(playerhand, dealerfacecard):
                cases_hit.append((player_val, dealer_val))
                hit()
            else:
                cases_stand.append((player_val, dealer_val))
                stand()
        if game_result == 1:
            player_wins += 1
            for case in cases_hit:
                table[case][0] += 2
            for case in cases_stand:
                table[case][1] += 2
        if game_result == 0:
            for case in cases_hit:
                table[case][0] -= 1
            for case in cases_stand:
                table[case][1] -= 1

def play(times):
    global player_wins
    for _ in range(times):
        deal()
        while(in_play):
            if hitme(playerhand, dealerfacecard):
                hit()
            else:
                stand()
        if game_result == 1:
            player_wins += 1
    winning_percentage = player_wins / times
    print("Decision Table")
    print(table)
    print("Final Score is {}".format(score))
    print("Player Wins {} times".format(player_wins))
    print("Winning Percentage is {}%".format(winning_percentage*100))

table_init()
#sim(1000000)
sim(100000)
player_wins = 0
score = 0
in_play = False
play(100000)