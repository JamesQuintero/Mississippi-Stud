#
# Copyright (c) James Quintero 2020
#
# Last Modified: 12/2022
#

# Simulates playing with certain hands

import json
import csv
import os
import copy
import random

from HandStrength import HandStrength
from Utils import Utils


class Simulate:

    hand_strength = None

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
    Simulates the player having certain types of hands, like pairs, or one high card and one low card, etc. The stats should be the same between Kx5x and Jx2x since they are both one high and one low card. 
    """
    def simulate_important_cards(self):
        player_hands = [
            ["13s", "13c"], #Winning pair
            ["13s", "12c"], #Two winning cards
            ["13c", "12c"], #Two winning cards suited
            ["13s", "9c"], #Winning card and push card
            ["13c", "9c"], #Winning card and push card suited
            ["13s", "5c"], #Winning card and losing card
            ["13c", "5c"], #Winning card and losing card suited

            ["9s", "9c"], #Pushing pair
            ["9s", "8c"], #Two pushing cards
            ["9c", "8c"], #Two pushing cards suited
            ["9s", "5c"], #Push card and losing card
            ["9c", "5c"], #Push card and losing card suited

            ["5s", "5c"], #Losing pair
            ["5s", "4c"], #Two losing cards
            ["5c", "4c"], #Two losing cards suited
        ]

        cards_to_remove = [
            []
        ] * len(player_hands)

        num_runs = int(input("Num runs: "))

        self.simulate(num_runs, player_hands, cards_to_remove)


    """
    Simulate change in odds if player has middle cards and other players have a lot of over cards.
    """
    def simulate_over_cards(self):
        player_hands = [
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
        ]

        cards_to_remove = [
            [],
            ["11x"], #Sees 1 over card
            ["11x", "14x", "13x"], #Sees 3 over cards
            ["11x", "14x", "13x", "12x", "11x", "14x"], #Sees 6 over cards
            ["11x", "14x", "13x", "12x", "11x", "14x", "13x", "12x"], #Sees 8 over cards
            ["11x", "14x", "13x", "12x", "11x", "14x", "13x", "12x", "11x", "14x"], #Sees 10 over cards
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_over_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)


    """
    Simulate change in odds if player has middle cards and other players have a lot of lower cards
    """
    def simulate_under_cards(self):
        player_hands = [
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
            ["10c", "9d"], #Two middle cards
        ]

        cards_to_remove = [
            [],
            ["2x"], #Sees 1 under card
            ["2x", "5x", "3x"], #Sees 3 under cards
            ["2x", "5x", "3x", "4x", "2x", "5x"], #Sees 6 under cards
            ["2x", "5x", "3x", "4x", "2x", "5x", "3x", "4x"], #Sees 8 under cards
            ["2x", "5x", "3x", "4x", "2x", "5x", "3x", "4x", "2x", "5x"], #Sees 10 under cards
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_under_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)

    """
    Simulates change in odds if you see whether other players do or do not have the same high card.
    """
    def simulate_high_cards(self):
        player_hands = [
            ["13c", "11d"], #Two high cards
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card
            ["13c", "11d"], #Two high card

            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
            ["13c", "2d"], #One high card
        ]

        cards_to_remove = [
            [],
            ["13x"], #See 1 card is same
            ["13x", "13x"], #See 2 cards are the same
            ["13x", "13x", "13x"], #See 3 other cards are the same
            ["2x"], #See 1 card not same type
            ["2x", "14x", "3x"], #See 3 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x"], #See 6 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x", "5x", "9x"], #See 8 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x", "5x", "9x", "6x", "8x"], #See 10 cards not same type
            [],
            ["13x"], #See 1 card is same
            ["13x", "13x"], #See 2 cards are the same
            ["13x", "13x", "13x"], #See 3 other cards are the same
            ["2x"], #See 1 card not same type
            ["2x", "14x", "3x"], #See 3 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x"], #See 6 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x", "5x", "9x"], #See 8 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "10x", "5x", "9x", "6x", "8x"], #See 10 cards not same type
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_high_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)


    """
    Simulates change in odds if you see whether other players do or do not have the same middle cards.
    """
    def simulate_middle_cards(self):
        player_hands = [
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
            ["10c", "6d"], #Two middle cards
        ]

        cards_to_remove = [
            [],
            ["10x"], #See 1 card is same
            ["10x", "10x"], #See 2 cards are the same
            ["10x", "10x", "10x"], #See 3 other cards are the same
            ["10x", "6x"], #See 2 cards are the same
            ["10x", "6x", "10x", "6x"], #See 3 other cards are the same
            ["2x"], #See 1 card not same type
            ["2x", "14x", "3x"], #See 3 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "11x"], #See 6 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "11x", "5x", "9x"], #See 8 cards not same type
            ["2x", "14x", "3x", "12x", "4x", "11x", "5x", "9x", "7x", "8x"], #See 10 cards not same type
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_middle_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)


    """
    Simulates change in odds if you see whether other players do or do not have the same middle cards.
    """
    def simulate_low_cards(self):
        player_hands = [
            ["5c", "2d"], #Two low cards
            ["5c", "2d"], #Two low cards
            ["5c", "2d"], #Two low cards
            ["5c", "2d"], #Two low cards
            ["5c", "2d"], #Two low cards
            ["5c", "2d"], #Two low cards
        ]

        cards_to_remove = [
            [],
            ["3x"], #See 1 card not same type
            ["3x", "14x", "3x"], #See 3 cards not same type
            ["3x", "14x", "3x", "12x", "4x", "11x"], #See 6 cards not same type
            ["3x", "14x", "3x", "12x", "4x", "11x", "6x", "9x"], #See 8 cards not same type
            ["3x", "14x", "3x", "12x", "4x", "11x", "6x", "9x", "7x", "8x"], #See 10 cards not same type
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_low_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)


    """
    No matter the hand, each suited hand has the same chance of getting a flush, so simulate that chance depending on seeing other player's cards.
    """
    def simulate_flushes(self):
        player_hands = [
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
            ["5c", "4c"], #Two losing cards suited
        ]

        cards_to_remove = [
            [],
            ["Xc"], #See 1 card with same suit
            ["Xc", "Xc", "Xc"], #See 3 cards with same suit
            ["Xc", "Xc", "Xc", "Xc", "Xc", "Xc"], #See 6 cards with same suit
            ["Xd"], #See 1 card without same suit
            ["Xd", "Xs", "Xh"], #See 3 cards with same suit
            ["Xd", "Xs", "Xh", "Xd", "Xs", "Xh"], #See 6 cards with same suit
            ["Xd", "Xs", "Xh", "Xd", "Xs", "Xh", "Xd", "Xs"], #See 8 cards with same suit
            ["Xd", "Xs", "Xh", "Xd", "Xs", "Xh", "Xd", "Xs", "Xh", "Xd"], #See 10 cards with same suit
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_flush_cards_{}.csv".format(num_runs, play_style)
        self.simulate(num_runs, player_hands, cards_to_remove, play_optimally=play_optimally, save_path=save_path)


    """
    Simulates the player having all combinations of hands. 
    """
    def simulate_all_cards(self):
        player_hands = [
            ["14s", "14c"],
            ["14s", "13c"],
            ["14s", "12c"],
            ["14s", "11c"],
            ["14s", "10c"],
            ["14s", "9c"],
            ["14s", "8c"],
            ["14s", "7c"],
            ["14s", "6c"],
            ["14s", "5c"],
            ["14s", "4c"],
            ["14s", "3c"],
            ["14s", "2c"],

            ["13s", "13c"],
            ["13s", "12c"],
            ["13s", "11c"],
            ["13s", "10c"],
            ["13s", "9c"],
            ["13s", "8c"],
            ["13s", "7c"],
            ["13s", "6c"],
            ["13s", "5c"],
            ["13s", "4c"],
            ["13s", "3c"],
            ["13s", "2c"],

            ["12s", "12c"],
            ["12s", "11c"],
            ["12s", "10c"],
            ["12s", "9c"],
            ["12s", "8c"],
            ["12s", "7c"],
            ["12s", "6c"],
            ["12s", "5c"],
            ["12s", "4c"],
            ["12s", "3c"],
            ["12s", "2c"],

            ["11s", "11c"],
            ["11s", "10c"],
            ["11s", "9c"],
            ["11s", "8c"],
            ["11s", "7c"],
            ["11s", "6c"],
            ["11s", "5c"],
            ["11s", "4c"],
            ["11s", "3c"],
            ["11s", "2c"],

            ["10s", "10c"],
            ["10s", "9c"],
            ["10s", "8c"],
            ["10s", "7c"],
            ["10s", "6c"],
            ["10s", "5c"],
            ["10s", "4c"],
            ["10s", "3c"],
            ["10s", "2c"],

            ["9s", "9c"],
            ["9s", "8c"],
            ["9s", "7c"],
            ["9s", "6c"],
            ["9s", "5c"],
            ["9s", "4c"],
            ["9s", "3c"],
            ["9s", "2c"],

            ["8s", "8c"],
            ["8s", "7c"],
            ["8s", "6c"],
            ["8s", "5c"],
            ["8s", "4c"],
            ["8s", "3c"],
            ["8s", "2c"],

            ["7s", "7c"],
            ["7s", "6c"],
            ["7s", "5c"],
            ["7s", "4c"],
            ["7s", "3c"],
            ["7s", "2c"],

            ["6s", "6c"],
            ["6s", "5c"],
            ["6s", "4c"],
            ["6s", "3c"],
            ["6s", "2c"],

            ["5s", "5c"],
            ["5s", "4c"],
            ["5s", "3c"],
            ["5s", "2c"],

            ["4s", "4c"],
            ["4s", "3c"],
            ["4s", "2c"],

            ["3s", "3c"],
            ["3s", "2c"],

            ["2s", "2c"],

            #Suited
            ["14c", "13c"],
            ["14c", "12c"],
            ["14c", "11c"],
            ["14c", "10c"],
            ["14c", "9c"],
            ["14c", "8c"],
            ["14c", "7c"],
            ["14c", "6c"],
            ["14c", "5c"],
            ["14c", "4c"],
            ["14c", "3c"],
            ["14c", "2c"],

            ["13c", "12c"],
            ["13c", "11c"],
            ["13c", "10c"],
            ["13c", "9c"],
            ["13c", "8c"],
            ["13c", "7c"],
            ["13c", "6c"],
            ["13c", "5c"],
            ["13c", "4c"],
            ["13c", "3c"],
            ["13c", "2c"],

            ["12c", "11c"],
            ["12c", "10c"],
            ["12c", "9c"],
            ["12c", "8c"],
            ["12c", "7c"],
            ["12c", "6c"],
            ["12c", "5c"],
            ["12c", "4c"],
            ["12c", "3c"],
            ["12c", "2c"],

            ["11c", "10c"],
            ["11c", "9c"],
            ["11c", "8c"],
            ["11c", "7c"],
            ["11c", "6c"],
            ["11c", "5c"],
            ["11c", "4c"],
            ["11c", "3c"],
            ["11c", "2c"],

            ["10c", "9c"],
            ["10c", "8c"],
            ["10c", "7c"],
            ["10c", "6c"],
            ["10c", "5c"],
            ["10c", "4c"],
            ["10c", "3c"],
            ["10c", "2c"],

            ["9c", "8c"],
            ["9c", "7c"],
            ["9c", "6c"],
            ["9c", "5c"],
            ["9c", "4c"],
            ["9c", "3c"],
            ["9c", "2c"],

            ["8c", "7c"],
            ["8c", "6c"],
            ["8c", "5c"],
            ["8c", "4c"],
            ["8c", "3c"],
            ["8c", "2c"],

            ["7c", "6c"],
            ["7c", "5c"],
            ["7c", "4c"],
            ["7c", "3c"],
            ["7c", "2c"],

            ["6c", "5c"],
            ["6c", "4c"],
            ["6c", "3c"],
            ["6c", "2c"],

            ["5c", "4c"],
            ["5c", "3c"],
            ["5c", "2c"],

            ["4c", "3c"],
            ["4c", "2c"],

            ["3c", "2c"]
        ]


        cards_to_remove = [
            []
        ] * len(player_hands)

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"

        self.simulate(num_runs, player_hands, cards_to_remove=cards_to_remove, play_optimally=play_optimally)


    """
    Runs through all provided player hands to simulate many games for each hand.
    """
    def simulate(self, num_runs = None, player_hands=[], board=[], cards_to_remove=[], play_optimally=None, save_path=None):
        if num_runs == None:
            num_runs = int(input("Num runs: "))

        if play_optimally == None:
            play_optimally = input("Play optimally? (y/n): ").lower() == "y"

        to_save = [self.util.get_header()]
        for x in range(0, len(player_hands)):
            num_player_wins, num_dealer_wins, num_pushes, total_profit, ending_bankroll, hand_strengths = self.simulate_many_runs(num_runs, play_optimally, player_hand=player_hands[x], board=board, cards_to_remove=cards_to_remove[x])

            row = [
                ','.join(self.util.convert_cards(player_hands[x])),
                ','.join(self.util.convert_cards(cards_to_remove[x])),
                self.util.convert_number(num_player_wins/num_runs),
                self.util.convert_number(num_dealer_wins/num_runs),
                self.util.convert_number(num_pushes/num_runs),
                self.util.convert_number(total_profit/num_runs),
                ending_bankroll
            ]
            row.extend([ (hand_strengths[key]/num_runs*100) for key in hand_strengths ])

            to_save.append(row)

        if play_optimally:
            play_style = "optimal_play"
        else:
            play_style = "play_to_end"

        if save_path == None:
            save_path = "./Results/simulate_{}_runs_{}_cards_{}.csv".format(num_runs, len(player_hands), play_style)
        self.util.save_to_csv(save_path, to_save)


    """
    Simulates one game many times given the starting player_hand
    """
    def simulate_many_runs(self, num_runs = 1000000, play_optimally=True, player_hand=[], board=[], cards_to_remove=[]):

        if len(player_hand) != 0:
            print("Starting player hand: "+str(self.util.convert_cards(player_hand)))
        if len(cards_to_remove) != 0:
            print("Cards in other player's hand: {}".format(self.util.convert_cards(cards_to_remove)))


        self.reset()

        num_player_wins = 0
        num_dealer_wins = 0
        num_pushes = 0
        total_profit = 0

        for x in range(0, num_runs):

            starting_bankroll = self.bankroll

            winner = self.simulate_single(play_optimally, player_hand=player_hand, board=board, cards_to_remove=cards_to_remove)

            #player wins with pair of jacks or better
            if winner == 1:
                num_player_wins += 1
                player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
                self.bankroll += sum(self.bets)*self.util.payout[player_hand_strength[0]]

            #pushes with pair of 6s to pair of 10s
            elif winner == 0:
                num_pushes += 1
                self.bankroll += sum(self.bets)

            #player lost
            else:
                num_dealer_wins += 1


            ending_bankroll = self.bankroll
            bankroll_diff = ending_bankroll - starting_bankroll
            total_profit += bankroll_diff



            if x != 0 and x % 100000 == 0:
                print("Hand #"+str(x))


        self.util.print_bankroll_state(self.starting_bankroll, self.bankroll, self.bet_amount)

        print("Num player wins: {:,}".format(num_player_wins))
        print("Num dealer wins: {:,}".format(num_dealer_wins))
        print("Num pushes: {:,}".format(num_pushes))
        print("Win %: {:.2f}%".format(num_player_wins/num_runs*100))
        print("Lose %: {:.2f}%".format(num_dealer_wins/num_runs*100))
        print("Push %: {:.2f}%".format(num_pushes/num_runs*100))
        print("Avg return per hand: ${:,.2f}".format(total_profit/num_runs))
        print()
        self.util.print_hand_strength_distribution(self.hand_strength_distribution, num_runs)
        print()

        return num_player_wins, num_dealer_wins, num_pushes, total_profit, self.bankroll, copy.deepcopy(self.hand_strength_distribution)


    """
    Simulates one game many times given the starting player_hand
    """
    def simulate_many_runs_multiprocessing(self, num_runs = 1000, play_optimally=True, player_hand=[], board=[], cards_to_remove=[]):

        if player_hand != None and len(player_hand) != 0:
            print("Starting player hand: "+str(self.util.convert_cards(player_hand)))
        if cards_to_remove != None and len(cards_to_remove) != 0:
            print("Cards in other player's hand: {}".format(self.util.convert_cards(cards_to_remove)))


        self.reset()

        num_player_wins = 0
        num_dealer_wins = 0
        num_pushes = 0
        total_profit = 0

        import multiprocessing

        parameters = [(play_optimally, player_hand, board, cards_to_remove) for _ in range(num_runs)]

        num_processors = 32
        pool = multiprocessing.Pool(num_processors)
        results = pool.starmap(self.simulate_single_full, parameters)
        pool.close()
        pool.join()

        # Initialize the variables
        num_player_wins = 0
        num_dealer_wins = 0
        num_pushes = 0
        total_profit = 0

        # Iterate over the results and update the variables
        for result in results:
            winner, bankroll_diff, player_hand_strength = result

            #player wins with pair of jacks or better
            if winner == 1:
                self.hand_strength_distribution[player_hand_strength] += 1
                num_player_wins += 1

            #pushes with pair of 6s to pair of 10s
            elif winner == 0:
                self.hand_strength_distribution[player_hand_strength] += 1
                num_pushes += 1

            #player lost
            else:
                num_dealer_wins += 1

            self.bankroll += bankroll_diff
            total_profit += bankroll_diff


        # ending_bankroll = self.bankroll
        # bankroll_diff = ending_bankroll - starting_bankroll
        # total_profit += bankroll_diff



        # if x != 0 and x % 100000 == 0:
        #     print("Hand #"+str(x))


        # self.util.print_bankroll_state(self.starting_bankroll, self.bankroll, self.bet_amount)

        # print("Num player wins: {:,}".format(num_player_wins))
        # print("Num dealer wins: {:,}".format(num_dealer_wins))
        # print("Num pushes: {:,}".format(num_pushes))
        # print("Win %: {:.2f}%".format(num_player_wins/num_runs*100))
        # print("Lose %: {:.2f}%".format(num_dealer_wins/num_runs*100))
        # print("Push %: {:.2f}%".format(num_pushes/num_runs*100))
        # print("Avg return per hand: ${:,.2f}".format(total_profit/num_runs))
        # print()
        # self.util.print_hand_strength_distribution(self.hand_strength_distribution, num_runs)
        # print()

        return num_player_wins, num_dealer_wins, num_pushes, total_profit, self.bankroll, copy.deepcopy(self.hand_strength_distribution)


    """
    Returns change in bankroll
    """
    def simulate_single_full(self, play_optimally=True, player_hand=None, board=[], cards_to_remove=[]):
        starting_bankroll = self.bankroll

        winner = self.simulate_single(play_optimally, player_hand=player_hand, board=board, cards_to_remove=cards_to_remove)

        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
        # player_hand_strength = [0, 0]

        #player wins with pair of jacks or better
        if winner == 1:
            self.bankroll += sum(self.bets)*self.util.payout[player_hand_strength[0]]

            ending_bankroll = self.bankroll
            bankroll_diff = ending_bankroll - starting_bankroll

            return 1, bankroll_diff, player_hand_strength[0]

        #pushes with pair of 6s to pair of 10s
        elif winner == 0:
            self.bankroll += sum(self.bets)
            ending_bankroll = self.bankroll
            bankroll_diff = ending_bankroll - starting_bankroll

            return 0, bankroll_diff, player_hand_strength[0]

        #player lost
        else:
            return -1, -sum(self.bets), 0


    """
    Simulates a single game. Returns 1 if player wins, -1 if dealer wins, and 0 if push
    """
    def simulate_single(self, play_optimally=True, player_hand=None, board=[], cards_to_remove=[]):

        #shuffles the deck of cards
        self.deck = self.util.initialize_deck()

        #make bets
        self.initial_bets()

        #player gets random cards
        if player_hand == None or len(player_hand) == 0:
            self.player_hand[0] = self.deck.pop()
            self.player_hand[1] = self.deck.pop()
        #player gets certain cards
        else:
            self.player_hand = player_hand
            self.deck.pop(self.deck.index(self.player_hand[0]))
            self.deck.pop(self.deck.index(self.player_hand[1]))

        #Remove cards that you would see in other player's hands
        for card in cards_to_remove:
            try:
                #If type of card is wild, choose random card of that suit
                if "X" in card:
                    card = self.util.get_cards_same_suit(self.deck, num_cards=1, suit=self.util.get_suit(card))[0]
                #If suit is wild, choose random card of that type
                elif "x" in card:
                    card = self.util.get_cards_same_type(self.deck, num_cards=1, type=self.util.get_type(card))[0]

                self.deck.pop(self.deck.index(card))
            except Exception as error:
                input("Error: {}".format(error))
                pass

        #Shuffles since we might have removed flush cards from the bottom of the deck.
        random.shuffle(self.deck)


        #deal rest of cards
        self.deal(initial_board=board)

        if play_optimally:
            #player bets optimally, according to wizard-of-odds
            self.play_optimally()
        else:
            # self.play_3rd_str_then_optimally()
            self.play_until_end()



        #if player folded, just skip to the next hand
        if self.fold:
            return -1



        # dealer_hand_strength = self.determine_hand_strength(self.board, self.dealer_hand)
        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

        #player wins with pair of jacks or better
        if player_hand_strength[0] >= 2 or (player_hand_strength[0] == 1 and player_hand_strength[1][0]>=11):
            self.hand_strength_distribution[player_hand_strength[0]] += 1
            return 1

        #pushes with pair of 6s to pair of 10s
        elif player_hand_strength[0] == 1 and player_hand_strength[1][0]>=6:
            self.hand_strength_distribution[player_hand_strength[0]] += 1
            return 0

        #player lost
        else:
            #Only want to save high card hands, because any other hand is a losing pair, and don't want to save that.
            if player_hand_strength[0] == 0:
                self.hand_strength_distribution[player_hand_strength[0]] += 1
            return -1

    """
    Plays optimally according to wizard-of-odds

    Looking at player's hand, every street is bet in a way to simulate actual gameplay
    Ante is already bet
    """
    def play_optimally(self):

        if self.verbose:
            print("Player's hand: "+str(self.player_hand))
            board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
            print("Board: {}".format(board_to_print))

        sorted_player_hand = sorted(self.player_hand)

        success = self.bet_3rd_street(sorted_player_hand)
        if not success:
            return 

        success = self.bet_4th_street()
        if not success:
            return

        success = self.bet_5th_street()
        if not success:
            return

    """
    Plays 3rd street no matter what, then plays optimally according to wizard-of-odds

    Looking at player's hand, every street is bet in a way to simulate actual gameplay
    Ante is already bet
    """
    def play_3rd_str_then_optimally(self):

        if self.verbose:
            print("Player's hand: "+str(self.player_hand))
            board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
            print("Board: {}".format(board_to_print))

        #Bets 3rd street no matter what
        self.bet(1, self.bet_amount)

        success = self.bet_4th_street()
        if not success:
            return

        success = self.bet_5th_street()
        if not success:
            return


    """
    Plays and never folds.
    Bets minimum, although this method should only be used to calculate win-rate and not avg return. 
    """
    def play_until_end(self):

        if self.verbose:
            print("Player's hand: "+str(self.player_hand))
            board_to_print = ",".join([ self.util.convert_card(card) for card in self.board ])
            print("Board: {}".format(board_to_print))

        sorted_player_hand = sorted(self.player_hand)

        self.bet(1, self.bet_amount)
        self.bet(2, self.bet_amount)
        self.bet(3, self.bet_amount)


    """
    Returns the basic strategy move for 3rd street (1st community card)

    Strategy from wizardofodds.com
    """
    def move_3rd_street(self, sorted_player_hand, player_hand, board):
        ###
        #bets 3rd street
        #To bet 3rd street, you can only see your cards, which is street="ante"
        # Strategy
        # - Raise 3x with any pair.
        # - Raise 1x with at least two points.
        # - Raise 1x with 6/5 suited.
        # Fold all others.

        points = self.get_num_points(street="ante", player_hand=player_hand, board=board)

        hand_strength = self.hand_strength.determine_hand_strength(board=[], hand=player_hand)

        #Raise 3x with any pair
        if hand_strength[0] == 1:
            return 2
        elif hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            return 2
        #raise 1x with at least 2 points
        elif points>=2:
            return 1
        #Raise 1x with 6/5 suited
        elif sorted_player_hand[0][0]==5 and sorted_player_hand[1][0]==6 and sorted_player_hand[0][1]==sorted_player_hand[1][1]:
            return 1
        else:
            return -1


    def move_4th_street(self, player_hand, board):
        ###
        # bets 4th card (4th street)
        # To bet 2nd street, you can only see your cards and the first board card, which is street="3rd"
        # - Raise 3x with any made hand (mid pair or higher).
        # ?- Raise 3x with royal flush draw.
        # ?- Raise 3x with straight flush draw, with no gaps, 567 or higher.
        # ?- Raise 3x with straight flush draw, with one gap, and at least one high card.
        # ?- Raise 3x with straight flush draw, with two gaps, and at least two high cards.
        # - Raise 1x with any other three suited cards.
        # - Raise 1x with a low pair.
        # - Raise 1x with at least three points.
        # Raise 1x with a straight draw, with no gaps, 456 or higher.
        # Raise 1x with a straight draw, with one gap, and two mid cards.
        # - Fold all others.

        points = self.get_num_points(street="3rd", player_hand=player_hand, board=board)

        hand_strength = self.hand_strength.determine_hand_strength(board=[board[0]], hand=player_hand)

        #Raise 3x with any made hand (mid pair or higher)
        if hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            return 2
        #Raise 1x with a low pair
        elif hand_strength[0]==1:
            return 1
        #raise 1x with at least 3 points
        elif points>=3:
            return 1
        #Raise 1x with any other three suited cards
        elif self.util.get_suit(player_hand[0])==self.util.get_suit(player_hand[1]) and self.util.get_suit(player_hand[1])==self.util.get_suit(board[0]):
            return 1
        #Fold all others
        else:
            return -1


    def move_5th_street(self, player_hand, board, bets):
        ###
        # bets 5th card (5th street)
        # - Raise 3x with any made hand (mid pair or higher).
        # - Raise 3x with any four to a flush.
        # Raise 3x with four to an outside straight, 8 high or better.
        # Raise 1x with any other straight draw.
        # - Raise 1x with a low pair.
        # - Raise 1x with at least four points.
        # - Raise 1x with three mid cards and at least one previous 3x raise.
        # - Fold all others.

        if len(board) < 2:
            print("Error when determing move for 5th street, board is not proper length. {} vs expected 2".format(len(board)))

        points = self.get_num_points(street="4th", player_hand=player_hand, board=board)

        hand_strength = self.hand_strength.determine_hand_strength(board=board[0:2], hand=player_hand)

        
        #Raise 3x with any made hand (mid pair or higher)
        if hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            return 2
        #Raise 3x with any four to a flush
        elif self.util.get_suit(player_hand[0])==self.util.get_suit(player_hand[1]) and \
            self.util.get_suit(player_hand[1])==self.util.get_suit(board[0]) and \
            self.util.get_suit(player_hand[1])==self.util.get_suit(board[1]):
            return 2
        #Raise 1x with a low pair
        elif hand_strength[0]==1:
            return 1
        #raise 1x with at least 4 points or Raise 1x with three mid cards and at least one previous 3x raise
        elif points >= 4 or (points>=3 and self.bet_amount*3 in bets):
            return 1
        #Fold all others
        else:
            return -1

        

    """
    Basic strategy way to play 3rd street (1st community card)
    """
    def bet_3rd_street(self, sorted_player_hand):
        move = self.move_3rd_street(sorted_player_hand, self.player_hand, self.board)

        # Bet 3x
        if move == 2:
            bet_amount = self.bet_amount*3
        # Bet 1x
        elif move == 1:
            bet_amount = self.bet_amount
        # Fold
        elif move == -1:
            self.fold = True
            return False

        self.bet(1, bet_amount)

        return True
    
    """
    Basic strategy way to play 4th street (2nd community card)
    """
    def bet_4th_street(self):
        move = self.move_4th_street(self.player_hand, self.board)

        # Bet 3x
        if move == 2:
            bet_amount = self.bet_amount*3
        # Bet 1x
        elif move == 1:
            bet_amount = self.bet_amount
        # Fold
        elif move == -1:
            self.fold = True
            return False

        self.bet(2, bet_amount)

        return True

    """
    Basic strategy way to play 5th street (3rd community card)
    """
    def bet_5th_street(self):
        move = self.move_5th_street(self.player_hand, self.board, self.bets)

        # Bet 3x
        if move == 2:
            bet_amount = self.bet_amount*3
        # Bet 1x
        elif move == 1:
            bet_amount = self.bet_amount
        # Fold
        elif move == -1:
            self.fold = True
            return False

        self.bet(3, bet_amount)








    """
    Returns the number of "points" the player has. 
    Points are calculated according to wizard-of-odds. 


    High = J to A = 2 points
    Mid = 6 to 10 = 1 point
    Low = 2 to 5 = 0 points

    street values = ["ante", "3rd", "4th", "5th"]
    """
    def get_num_points(self, street="ante", player_hand=[], board=[]):

        #only want points of player's hand
        if street == "ante":
            cards = player_hand

        #want points of player's hand and first card of board
        elif street == "3rd":
            try:
                cards = board[0:1] + player_hand
            except Exception as error:
                print("Error, {}".format(error))

        #want points of player's hand and first two cards of board
        elif street == "4th":
            try:
                cards = board[0:2] + player_hand
            except Exception as error:
                print("Error, {}".format(error))

        #want points of player's hand and first two cards of board
        elif street == "5th":
            cards = board + player_hand

        #gets points of all cards
        points = 0
        for card in cards:
            value = int(card[:-1])

            #J-A are 2 points
            if value >= 11:
                points += 2
            #6-10 are 1 point
            elif value >= 6:
                points += 1
            #2-5 are 0 points
            else:
                points += 0

        return points

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

    """
    deals community cards

    board only has 3 cards in mississippi stud
    """
    def deal(self, initial_board=[]):

        # print("Dealing! Initial board: {}".format(initial_board))
        # print("Current board: {}".format(self.board))
        # print("Deck size: {}".format(len(self.deck)))
        self.board = copy.copy(initial_board)

        #Removes used cards from deck
        for card in initial_board:
            self.deck.remove(card)

        
        # print(self.board)

        #Deals remaining board
        while len(self.board) < 3:
            self.board.append(self.deck.pop())

        # print("Self.board now: {}".format(self.board))
        # input("what")
        

if __name__=="__main__":
    simulate = Simulate()
    # simulate.simulate_high_cards()
    # simulate.simulate_over_cards()
    # simulate.simulate_under_cards()
    # simulate.simulate_middle_cards()
    # simulate.simulate_low_cards()

    # simulate.simulate_single(play_optimally=False, player_hand=["10c", "2c"], board=["8h", "6d", "8s"], cards_to_remove=[])
    # simulate.simulate_many_runs(num_runs = 100000, play_optimally=True, player_hand=['8d', '12c'], board=[], cards_to_remove=['9s', '4h', '4d', '2h', '12d', '2d'])
    # simulate.util.print_current_state(simulate.board, simulate.player_hand, simulate.other_players_hands, simulate.bets, simulate.starting_bankroll, simulate.bankroll, simulate.bet_amount)

    import time
    start_time = time.perf_counter()
    simulate.simulate_many_runs_multiprocessing(num_runs = 100000, play_optimally=True, player_hand=None, board=[], cards_to_remove=[])
    end_time = time.perf_counter()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Convert the elapsed time to milliseconds
    elapsed_time_milliseconds = elapsed_time * 1000
    print("Elapsed time: ", elapsed_time_milliseconds, " milliseconds")