#
# Copyright (c) James Quintero 2022
#
# Last Modified: 12/2022
#

# Utils file

import json
import csv
import os
import copy
import random

from HandStrength import HandStrength


class Utils:

    #format: "index = hand value"
    #0 = high card
    #1 = pair
    #2 = 2-pair
    #3 = trips
    #4 = straight
    #5 = flush
    #6 = full house
    #7 = quads
    #8 = straight flush
    #9 = royal flush
    #index corresponds to hand strength, [index] is amount to multiply bet by
    payout = [
        0, #Loses, 0/1 + 1
        2, #Pair pays 1 to 1, 1/1 + 1
        3, #Two pair pays 2 to 1, 2/1 + 1
        4, #Trips pays 3 to 1, 3/1 + 1
        5, #Straight pays 4 to 1, 4/1 + 1
        7, #Flush pays 6 to 1, 6/1 + 1
        11, #Full House pays 10 to 1, 10/1 + 1
        41, #Quads pays 40 to 1, 40/1 + 1
        101, #Straight Flush pays 100 to 1, 100/1 + 1
        501 #Royal Flush pays 500 to 1, 500/1 + 1
    ]

    #if true, print statements are printed
    verbose = True


    


    def __init__(self):
        self.hand_strength = HandStrength()

        # self.reset()

        # self.verbose = False
        pass

    """
    Given the suit of card (ex: h, s), randomly find the specified number of them
    """
    def get_cards_same_suit(self, deck, num_cards, suit):
        cards = []
        for x in range(0, len(deck)):
            if self.get_suit(deck[x]) == suit:
                cards.append(deck[x])

            if len(cards) >= num_cards:
                break

        return cards

    """
    Given the type of card (ex: 13x), randomly find the specified number of them
    """
    def get_cards_same_type(self, deck, num_cards, type):
        cards = []
        for x in range(0, len(deck)):
            if self.get_type(deck[x]) == type:
                cards.append(deck[x])

            if len(cards) >= num_cards:
                break

        return cards


    """
    prints current state of the board and bets
    """
    def print_current_state(self, board, player_hand, other_players_hands, bets, starting_bankroll, bankroll, bet_amount):
        self.print_bankroll_state(starting_bankroll, bankroll, bet_amount)

        print("Ante bet: $"+str(bets[0]))
        print("3rd st bet: $"+str(bets[1]))
        print("4th st bet: $"+str(bets[2]))
        print("5th st bet: $"+str(bets[3]))

        self.print_board_state(board, player_hand, other_players_hands)

        player_hand_strength = self.hand_strength.determine_hand_strength(board, player_hand)
        print("Player hand strength: {}".format(self.hand_strength.convert_hand_strength(player_hand_strength)))

        print()


    """
    Prints the state of the bankroll, like amount, bet size.
    """
    def print_bankroll_state(self, starting_bankroll, current_bankroll, bet_amount):
        print()
        print("Starting bankroll: ${:,}".format(starting_bankroll))
        print("Bankroll: ${:,.2f}".format(current_bankroll))
        print("Bet size: ${:,}".format(bet_amount))
        print()
        

    """
    Prints the community cards and player hand
    """
    def print_board_state(self, board, player_hand, other_players_hands):
        print()
        board_to_print = ",".join([ self.convert_card(card) for card in board ])
        print("Board: {}".format(board_to_print))
        print("Player hand: {},{}".format(self.convert_card(player_hand[0]), self.convert_card(player_hand[1])))
        print()
        for x in range(0, len(other_players_hands)):
            print("Other player #{}'s hand: {}, {}".format(x+1, self.convert_card(other_players_hands[x][0]), self.convert_card(other_players_hands[x][1])))
        print()
        

    """
    Print distribution of each type of made hand, like % rates of pairs, two pairs, etc. 
    """
    def print_hand_strength_distribution(self, hand_strength_distribution, num_runs=None):
        #If don't specify number of runs, just print raw values
        if not num_runs:
            print(json.dumps(hand_strength_distribution, sort_keys=True, indent=4, default=str))
        #Print out rate that each hand type occurred
        else:
            new_hand_distribution = {}
            for key in hand_strength_distribution:
                new_hand_distribution[self.convert_hand_strength(key)] = "{:.2f}%".format(hand_strength_distribution[key]/num_runs*100)
            print(json.dumps(new_hand_distribution, indent=4, default=str))
            
    """
    Given the hand strength, convert to english version
    """
    def convert_hand_strength(self, hand_strength):
        to_return = {
            0: "High card",
            1: "Pair",
            2: "Two pair",
            3: "Trips",
            4: "Straight",
            5: "Flush",
            6: "Full House",
            7: "Quads",
            8: "Straight Flush",
            9: "Royal Flush"
        }

        #If provided in format of HandStrength
        if isinstance(hand_strength, list):
            return to_return[hand_strength[0]]
        else:
            return to_return[hand_strength]

    """
    Creates a random deck of 52 cards
    """
    def initialize_deck(self):

        #s = Spade
        #c = Club
        #h = Heart
        #d = Diamond
        deck = [
            "2s","2c","2h","2d", 
            "3s","3c","3h","3d", 
            "4s","4c","4h","4d", 
            "5s","5c","5h","5d",
            "6s","6c","6h","6d",  
            "7s","7c","7h","7d",  
            "8s","8c","8h","8d",  
            "9s","9c","9h","9d",  
            "10s","10c","10h","10d",  
            "11s","11c","11h","11d",  
            "12s","12c","12h","12d",  
            "13s","13c","13h","13d",  
            "14s","14c","14h","14d"
        ]
        random.shuffle(deck)

        return deck

    """
    Converts a list of cards into more user-friendly denotions. EX: 12s into Qs
    """
    def convert_cards(self, cards):
        to_return = []
        for x in range(0, len(cards)):
            to_return.append(self.convert_card(cards[x]))
        return to_return

    """
    Converts a card into more user-friendly denotion. EX: Turns 12s into Qs
    """
    def convert_card(self, card):

        before=[
            "2s","2c","2h","2d", 
            "3s","3c","3h","3d", 
            "4s","4c","4h","4d", 
            "5s","5c","5h","5d",
            "6s","6c","6h","6d",  
            "7s","7c","7h","7d",  
            "8s","8c","8h","8d",  
            "9s","9c","9h","9d",  
            "10s","10c","10h","10d",  
            "11s","11c","11h","11d",  
            "12s","12c","12h","12d",  
            "13s","13c","13h","13d",  
            "14s","14c","14h","14d"
        ]

        after=[
            "2s","2c","2h","2d", 
            "3s","3c","3h","3d", 
            "4s","4c","4h","4d", 
            "5s","5c","5h","5d",
            "6s","6c","6h","6d",  
            "7s","7c","7h","7d",  
            "8s","8c","8h","8d",  
            "9s","9c","9h","9d",  
            "10s","10c","10h","10d",  
            "Js","Jc","Jh","Jd",  
            "Qs","Qc","Qh","Qd",  
            "Ks","Kc","Kh","Kd",  
            "As","Ac","Ah","Ad"
        ]

        try:
            index = before.index(card)
        except Exception as error:
            return card

        return after[index]

    """
    Gets the suit from the card
    """
    def get_suit(self, card):
        return card[-1:]

    """
    Gets the type of card, like whether it's a 7, 11, or 2.
    """
    def get_type(self, card):
        return card[:-1]


    """
    Saves matrix to csv file
    """
    def save_to_csv(self, path, data):
        self.create_file_structure(path)

        with open(path, 'w', newline='') as file:
            contents = csv.writer(file)
            contents.writerows(data)

    """
    Receives a string of a path, iterates through the file structure, and creates directories if they don't yet exist. 
    Used for saving files where the whole path doesn't exist, so instead of failing, create the whole path
    """
    def create_file_structure(self, path):
        directories_only = os.path.dirname(path)

        # create directory if it does not exist
        if not os.path.exists(directories_only):
            os.makedirs(directories_only)

    """
    Clears the terminal screen
    """
    def clear_screen(self):
        if os.name == "nt":
            os.system("cls") #Clears the screen for Windows
        else:
            os.system("clear") #Clears the screen for Unix

    """
    CSV header of the results, column titles
    """
    def get_header(self):
        return [
            "Player's hand",
            "Other player's cards",
            "Win %",
            "Lose %",
            "Push %",
            "Avg profit $",
            "Ending bankroll $",
            "High Card %",
            "Pair %",
            "Two Pair %",
            "Trips %",
            "Straight %",
            "Flush %",
            "Full House %",
            "Quads %",
            "Straight Flush %",
            "Royal Flush %"
        ]

    """
    Converts 25.000000000000000001 to 25.0
    """
    def convert_number(self, number):

        try:
            #compensates for 24.9999999 turning into 24.9 instead of 25.0
            temp=(number+0.001)*100
            temp=int(temp)/100
            new=int(number*100)/100

            if new<temp:
                new=temp

            return new
        except Exception as error:
            print("Error converting number: "+str(error))
            return number