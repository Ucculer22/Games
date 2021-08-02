# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 11:28:56 2021

@author: cschm
"""

# War Game

# CARD
# SUIT, RANK, VALUE
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,
          'Eight':8, 'Nine':9, 'Ten':10,'Jack':11, 'Queen':12, 'King':13,
          'Ace':14}

playing = True


# CLASSES --------------------------------------------------------------------

# CREATE CARD CLASS
class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit
    
# CREATE DECK CLASS

class Deck():
    
    def __init__(self):
        
        # Empty list to add cards to
        self.deck = []
        
        # Add cards to empty deck
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))     
                
    def __str__(self):
        
        # Verify all cards that were added to the deck (should be 52)
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: "+ deck_comp
        
        
    def shuffle(self):
        
        # Shuffle the deck
        random.shuffle(self.deck)
        
    def deal(self):
        
        # Deal card to a player
        return self.deck.pop()
    
# CREATE HAND CLASS
        
class Hand():
    def __init__(self):
        self.cards = [] # start with an empty list as we did in the Deck Class
        self.value = 0 # start with a zero value
        self.aces = 0 # add an attribute to keep track of aces
        
    def add_card(self,card):
        
        # card passed in will be from class Deck.
        # from Deck.deal() --> single Card(suit,rank)
        
        self.cards.append(card)
        self.value += values[card.rank]
        
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        
        # Special Rule:
        # IF TOTAL VALUE > 21 & I STILL HAVE AN ACE
        # THAN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
# CREATE CHIPS CLASS
            
class Chips():
    
    def __init__(self,total=100):
        self.total = total # defulat value = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

# FUNCTIONS -------------------------------------------------------------------

# function to place a bet
def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Please provide an integer")
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! ' +
                      'You have: {}'.format(chips.total))
            else:
                break

# function for a "hit" in the game
def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace

# function to ask the player if they want to hit or stand    
def hit_or_stand(deck,hand):
    global playing # to control while loop
    
    while True:
        x = input('Hit or Stand? Enter h or s ')
        
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player STANDS. Dealer's Turn")
            playing = False
        else:
            print("Sorry wrong option. Hit or Stand? h or s ")
        break

# function to show the players hand
def show_some(player,dealer):
    
    # dealer.cards[0] and dealer.cards[1]
    
    # show only ONE of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])
    
    # show all (2 cards) of the player's hand/cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)


 # function to show all card
def show_all(player,dealer):
    
    # show all the dealer's cards
    print("\n Dealer's Hand: ")
    for card in dealer.cards:
        print(card)

    # calculate and display the value (i.e. J+K == 20)
    print(f"Value of Dealer's Hand is: {dealer.value}")
    
    # show all the player's cards
    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
    print(f"Value of Player's Hand is: {player.value}")
    
# GAME WIN/LOSE SITUATIONS ----------------------------------------------------
    
def player_busts(player,dealer,chips):
    print("BUST PLAYER!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS!")
    chips.win_bet()
    
def dealer_busts(player,dealer,chips):
    print("DEALER BUSTED! PLAYER WINS!")
    chips.win_bet()
    

def dealer_wins(player,dealer,chips):
    print("DEALER WINS! PLAYER LOST!")
    chips.lose_bet()
    

def push(player,dealer):
    print('TIE. Push')
    
# LOGIC -----------------------------------------------------------------------

while True:

    # print opening statement
    print('\n')
    print("Welcome to Python Black_Jack")
    print('\n')
    print('You start with 100 chips')
    
    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    # Player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    # Dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Set up the Player's Chips    
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    # recall this variable from our hit_or_stand function
    while playing:
        
        # Prompt for Player to either Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but again keep one dealer card hidden)
        show_all(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
        
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
            
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
            
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
            
        else:
            push(player_hand,dealer_hand)
        
    # Inform Player of their chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))
    
    # Ask to play again
    new_game = input("Would you like to play again??? Yes to continue: ")
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for Playing")
        break




















