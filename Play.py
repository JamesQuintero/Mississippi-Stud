#
# Copyright (c) James Quintero 2022
#
# Last Modified: 12/2022
#

#Play Mississippi Stud manually

import json
import csv
import os
import time
import copy
import random

from HandStrength import HandStrength
from Simulate import Simulate
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
    play_type = 0 #0 is manual, 1 is basic strategy, 2 is custom strategy

    deck = []
    board = []
    player_hand = []
    other_players_hands = [] #2D list of other player's hands at the table
    hand_strength_distribution = {}


    #if true, print statements are printed
    verbose = True


    


    def __init__(self):
        self.hand_strength = HandStrength()
        self.simulate = Simulate()
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
        # self.starting_bankroll = 200
        self.starting_bankroll = 100000

        self.reset()

        num_other_players = int(input("Number of other players playing: "))




        # auto_play = input("Auto Play? (y/n): ").lower() == "y"
        self.play_type = self.play_type_choice()

        num_rounds = 0
        max_rounds = 1000000
        while self.bankroll >= self.bet_amount and num_rounds <= max_rounds:
            self.play_round(num_other_players)
            num_rounds += 1

            if self.play_type == 1:
                self.util.clear_screen()
            self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)

            if self.play_type == 1:
                choice = input("Press any key to play again, (n) to cash out: ")
                if choice.lower() == "n":
                    break

            print("Finished round {}".format(num_rounds))

            self.reset_hand()

        print("Final bankroll: ${}".format(self.bankroll))
        print("Profit: ${}".format(self.bankroll - self.starting_bankroll))
        print("Number of hands played: {}".format(num_rounds))

    """
    Plays a single round of Mississippi Stud

    auto_play is True if AI will play instead of the user. 
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

        success = self.play_3rd_street()
        if not success:
            return self.player_lost()

        success = self.play_4th_street()
        if not success:
            return self.player_lost()

        success = self.play_5th_street()
        if not success:
            return self.player_lost()


        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        #player wins with pair of jacks or better
        if player_hand_strength[0] >= 2 or (player_hand_strength[0] == 1 and player_hand_strength[1][0]>=11):
            return self.player_won(player_hand_strength)

        #pushes with pair of 6s to pair of 10s
        elif player_hand_strength[0] == 1 and player_hand_strength[1][0]>=6:
            return self.player_pushes(player_hand_strength)

        #player lost
        else:
            return self.player_lost(player_hand_strength)


    def player_won(self, player_hand_strength=None):
        if player_hand_strength == None:
            player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        self.hand_strength_distribution[player_hand_strength[0]] += 1
        print("Won")
        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
        payout_multiplier = self.util.payout[player_hand_strength[0]]
        print("Payout {}x bets".format(payout_multiplier-1))
        self.bankroll += sum(self.bets)*self.util.payout[player_hand_strength[0]]
        return 1


    def player_pushes(self, player_hand_strength=None):
        if player_hand_strength == None:
            player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        self.hand_strength_distribution[player_hand_strength[0]] += 1
        print("Pushes")
        self.bankroll += sum(self.bets)
        return 0


    def player_lost(self, player_hand_strength=None):
        if player_hand_strength == None:
            player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        #Only want to save high card hands, because any other hand is a losing pair, and don't want to save that.
        if player_hand_strength[0] == 0:
            self.hand_strength_distribution[player_hand_strength[0]] += 1
        print("Lost")
        return -1


    """
    Plays 3rd street with the player betting and then the card being dealt
    """
    def play_3rd_street(self):
        ## 3rd street
        if self.play_type == 0:
            self.util.clear_screen()

        #Simulates possible outcomes
        print("Simulating expected avg return...")
        board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
        print("Board: {}".format(board_to_print))
        # num_runs = 10000
        # num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
        # expected_return = total_profit/num_runs
        # self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        # print("Recommended move: {}".format(self.recommended_move(expected_return)))

        if self.play_type == 1 or self.play_type == 3:
            num_runs = 100000
            num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
            expected_return = total_profit/num_runs

        # Manual play
        if self.play_type == 1:
            self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
            print("Recommended move: {}".format(self.recommended_move(expected_return)))
            choice = self.betting_choice()
        # Betting strategy
        elif self.play_type == 2:
            choice = self.basic_strategy(street=3)
        # Custom strategy
        elif self.play_type == 3:
            choice = self.recommended_move(expected_return)
        else:
            choice = self.betting_choice()
    
        
        #Raise 1x
        if choice == 1:
            self.bet(1, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(1, self.bet_amount*3)
        #Fold
        else:
            return False

        #Deals 3rd street
        self.board.append(self.deck.pop())

        return True


    """
    Plays 4th street with the player betting and then the card being dealt
    """
    def play_4th_street(self):
        ## 4th street
        if self.play_type == 1:
            self.util.clear_screen()
        print("Simulating expected avg return...")
        board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
        print("Board: {}".format(board_to_print))
        # num_runs = 10000
        # num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
        # expected_return = total_profit/num_runs
        # self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        # print("Recommended move: {}".format(self.recommended_move(expected_return)))

        if self.play_type == 1 or self.play_type == 3:
            num_runs = 100000
            num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
            expected_return = total_profit/num_runs

        # Manual play
        if self.play_type == 1:
            self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
            print("Recommended move: {}".format(self.recommended_move(expected_return)))
            choice = self.betting_choice()
        # Betting strategy
        elif self.play_type == 2:
            choice = self.basic_strategy(street=4)
        # Custom strategy
        elif self.play_type == 3:
            choice = self.recommended_move(expected_return)
        else:
            choice = self.betting_choice()

        # input("Move AI is going to make: {}. Continue?".format(choice))

        #Raise 1x
        if choice == 1:
            self.bet(2, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(2, self.bet_amount*3)
        #Fold
        else:
            return False

        #Deals 4th street
        self.board.append(self.deck.pop())

        return True

    """
    Plays 5th street with the player betting and then the card being dealt
    """
    def play_5th_street(self):
        ## 5th street
        if self.play_type == 1:
            self.util.clear_screen()
        print("Simulating expected avg return...")
        board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
        print("Board: {}".format(board_to_print))
        # num_runs = 10000
        # num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
        # expected_return = total_profit/num_runs
        # self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
        # print("Recommended move: {}".format(self.recommended_move(expected_return)))

        if self.play_type == 1 or self.play_type == 3:
            num_runs = 100000
            num_player_wins, num_dealer_wins, num_pushes, total_profit, bankroll, _ = self.simulate.simulate_many_runs(num_runs = num_runs, play_optimally=True, player_hand=copy.copy(self.player_hand), board=copy.copy(self.board), cards_to_remove=[ card for row in self.other_players_hands for card in row ])
            expected_return = total_profit/num_runs

        # Manual play
        if self.play_type == 1:
            self.util.print_current_state(self.board, self.player_hand, self.other_players_hands, self.bets, self.starting_bankroll, self.bankroll, self.bet_amount)
            print("Recommended move: {}".format(self.recommended_move(expected_return)))
            choice = self.betting_choice()
        # Betting strategy
        elif self.play_type == 2:
            choice = self.basic_strategy(street=5)
        # Custom strategy
        elif self.play_type == 3:
            choice = self.recommended_move(expected_return)
        else:
            choice = self.betting_choice()

        # input("Move AI is going to make: {}. Continue?".format(choice))
            
        #Raise 1x
        if choice == 1:
            self.bet(3, self.bet_amount)
        #Raise 3x
        elif choice == 2:
            self.bet(3, self.bet_amount*3)
        #Fold
        else:
            return False

        #Deals 5th street
        self.board.append(self.deck.pop())

        return True


    """
    expected_return is 
    
    Return 1 to 1x bet, 2 to 3x bet, -1 to fold.
    """
    def recommended_move(self, expected_return):
        print("Self.bets: {}".format(self.bets))
        print("Negative: {}".format(-sum(self.bets)))
        print("Expected return: {}".format(expected_return))
        if -sum(self.bets) < expected_return:
            print("Continue playing")
            #Betting 3x is probably the winning move
            # if sum(self.bets) <= expected_return:
            if expected_return >= self.bet_amount:
                print("Raise 3x")
                return 2
            #Betting 1x is the winning move
            else:
                return 1
        #Fold
        else:
            return -1


    def basic_strategy(self, street):
        if street == 3:
            sorted_player_hand = sorted(self.player_hand)
            return self.simulate.move_3rd_street(sorted_player_hand, player_hand=self.player_hand, board=self.board)
        elif street == 4:
            return self.simulate.move_4th_street(player_hand=self.player_hand, board=self.board)
        elif street == 5:
            return self.simulate.move_5th_street(player_hand=self.player_hand, board=self.board, bets=self.bets)
        else:
            print("Invalid street specified for basic strategy")
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
    User chooses what play style they want to initiate
    """
    def play_type_choice(self):
        choice = 0
        while choice < 1 or choice > 3:
            print()
            print("Play type choice: ")
            print("1) Manual (Player chooses the moves)")
            print("2) Auto basic strategy")
            print("3) Auto custom strategy")
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