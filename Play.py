#
# Copyright (c) James Quintero 2022
#
# Last Modified: 12/2022
#

#Play Mississippi Stud manually

import json
import csv
import os
import copy
import random

from HandStrength import HandStrength
from Utils import Utils

class Play:

    hand_strength = None
    util = None

    #Starting buy-in when sitting down at the table
    starting_bankroll = 1000000
    #min-bet is $15
    bet_amount = 10
    #[0] = Ante bet, [1] = 3rd street bet, [2] = 4th street bet, [3] = 5th street bet
    bets = [0,0,0,0]
    fold = False

    deck = []
    board = []
    player_hand = []
    other_players_hands = [] #2D list of other player's hands at the table
    hand_strength_distribution = {}


    #if true, print statements are printed
    verbose = True


    


    def __init__(self):
        self.hand_strength = HandStrength()
        self.util = Utils()

        self.reset()

        self.verbose = False

    """
    Sets up global variables
    """
    def reset(self):
        self.reset_hand()
        self.bankroll = self.starting_bankroll

        self.hand_strength_distribution = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
        }

    def reset_hand(self):
        self.board = []
        self.player_hand = [""]*2

    """
    Play a game of Mississippi Stud.
    """
    def play(self):
        self.starting_bankroll = 200

        self.reset()

        num_other_players = int(input("Number of other players playing: "))

        while self.bankroll >= self.bet_amount:
            self.play_round(num_other_players)
            self.util.clear_screen()
            self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
            choice = input("Press any key to play again, (n) to cash out: ")
            if choice.lower() == "n":
                break

            self.reset_hand()
        print("Final bankroll: ${}".format(self.bankroll))
        print("Profit: ${}".format(self.bankroll - self.starting_bankroll))

    """
    Plays a single round of Mississippi Stud
    """
    def play_round(self, num_other_players):
        #shuffles the deck of cards
        self.deck = self.util.initialize_deck()

        #make bets
        self.initial_bets()

        #player gets random cards
        self.player_hand[0] = self.deck.pop()
        self.player_hand[1] = self.deck.pop()

        #Deal to other players
        self.other_players_hands = []
        for x in range(num_other_players):
            self.other_players_hands.append([self.deck.pop(), self.deck.pop()])


        ## 3rd street
        self.util.clear_screen()
        self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        choice = self.betting_choice()
        #Raise 1x
        if choice == 1:
            self.bet(1, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(1, self.bet_amount*3)
        #Fold
        else:
            return -1

        #Deals 3rd street
        self.board.append(self.deck.pop())


        ## 4th street
        self.util.clear_screen()
        self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        choice = self.betting_choice()
        #Raise 1x
        if choice == 1:
            self.bet(2, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(2, self.bet_amount*3)
        #Fold
        else:
            return -1

        #Deals 4th street
        self.board.append(self.deck.pop())


        ## 5th street
        self.util.clear_screen()
        self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        choice = self.betting_choice()
        #Raise 1x
        if choice == 1:
            self.bet(3, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(3, self.bet_amount*3)
        #Fold
        else:
            return -1

        #Deals 5th street
        self.board.append(self.deck.pop())


        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        #player wins with pair of jacks or better
        if player_hand_strength[0] >= 2 or (player_hand_strength[0] == 1 and player_hand_strength[1][0]>=11):
            self.hand_strength_distribution[player_hand_strength[0]] += 1
            print("Won")
            player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
            payout_multiplier = self.util.payout[player_hand_strength[0]]
            print("Payout {}x bets".format(payout_multiplier-1))
            self.bankroll += sum(self.bets)*self.util.payout[player_hand_strength[0]]
            return 1

        #pushes with pair of 6s to pair of 10s
        elif player_hand_strength[0] == 1 and player_hand_strength[1][0]>=6:
            self.hand_strength_distribution[player_hand_strength[0]] += 1
            print("Pushes")
            self.bankroll += sum(self.bets)
            return 0

        #player lost
        else:
            #Only want to save high card hands, because any other hand is a losing pair, and don't want to save that.
            if player_hand_strength[0] == 0:
                self.hand_strength_distribution[player_hand_strength[0]] += 1
            print("Lost")
            return -1

    """
    Gets user input on what action to taken in regards to betting
    """
    def betting_choice(self):
        choice = 0
        while choice < 1 or choice > 3:
            print()
            print("Betting choice: ")
            print("1) Raise 1x")
            print("2) Raise 3x")
            print("3) Fold")
            try:
                choice = int(input("Choice: "))
            except:
                choice = 0

        return choice

    """
    places player's initial bets
    """
    def initial_bets(self):
        self.fold = False

        #ante bet
        self.bet(0, self.bet_amount)

        #reset the rest of the streets
        self.bets[1] = 0
        self.bets[2] = 0
        self.bets[3] = 0

    """
    player makets bet of size amount at time street
    """
    def bet(self, street, amount):
        self.bets[street] = amount
        self.bankroll -= amount


if __name__=="__main__":
    play = Play()
    play.play()