#
# Copyright (c) James Quintero 2020
#
# Last Modified: 12/2022
#

#determines best strategy for playing Mississippi Stud

import json
import csv
import os
import copy
import random

from HandStrength import HandStrength


class MississippiStud:

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
    # dealer_hand = []
    hand_strength_distribution = {}




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
    payout=[
        0, #pushes, 0/1 + 1
        2, #pays 1 to 1, 1/1 + 1
        3, #pays 2 to 1, 2/1 + 1
        4, #pays 3 to 1, 3/1 + 1
        5, #pays 4 to 1, 4/1 + 1
        7, #pays 6 to 1, 6/1 + 1
        11, #pays 10 to 1, 10/1 + 1
        41, #pays 40 to 1, 40/1 + 1
        101, #pays 100 to 1, 100/1 + 1
        501 #pays 500 to 1, 500/1 + 1
    ]

    #if true, print statements are printed
    verbose = True


    


    def __init__(self):
        self.hand_strength = HandStrength()

        self.reset()
        self.board = [""]*3
        self.player_hand = [""]*2

        self.verbose = False

    """
    Sets up global variables
    """
    def reset(self):
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


    """
    Provides menu to the user
    """
    def run(self):

        print("Menu: ")
        print("1) Play")
        print("2) Simulate")
        print("3) Give best strategy")

        choice = int(input("Choice: "))


        #play
        if(choice==1):
            print("Coming soon")

        #simulate
        if(choice==2):
            # self.simulate()
            # self.simulate_all_cards()
            # self.simulate_important_cards()
            # self.simulate_flushes()
            self.simulate_high_cards()

        #print best strategy
        if(choice==3):
            print("Nothing here, yet")

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
    Simulates change in odds if you see whether other players do or do not have the same high card.
    """
    def simulate_high_cards(self):
        player_hands = [
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
            ["13c", "11d"], #One high card
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
        ]

        num_runs = int(input("Num runs: "))
        play_optimally = input("Play optimally? (y/n): ").lower() == "y"


        play_style = "optimal_play" if play_optimally else "play_to_end"
        save_path = "./Results/simulate_{}_runs_high_cards_{}.csv".format(num_runs, play_style)
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

        self.simulate(num_runs, player_hands, cards_to_remove)


    """
    Runs through all provided player hands to simulate many games for each hand.
    """
    def simulate(self, num_runs = None, player_hands=[], cards_to_remove=[], play_optimally=None, save_path=None):
        if num_runs == None:
            num_runs = int(input("Num runs: "))

        if play_optimally == None:
            play_optimally = input("Play optimally? (y/n): ").lower() == "y"

        to_save = [self.get_header()]
        for x in range(0, len(player_hands)):
            num_player_wins, num_dealer_wins, num_pushes, total_profit, ending_bankroll, hand_strengths = self.simulate_many_runs(num_runs, play_optimally, player_hand=player_hands[x], cards_to_remove=cards_to_remove[x])

            row = [
                ','.join(self.convert_cards(player_hands[x])),
                ','.join(self.convert_cards(cards_to_remove[x])),
                self.convert_number(num_player_wins/num_runs),
                self.convert_number(num_dealer_wins/num_runs),
                self.convert_number(num_pushes/num_runs),
                self.convert_number(total_profit/num_runs),
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
        self.save_to_csv(save_path, to_save)


    """
    Simulates one game many times given the starting player_hand
    """
    def simulate_many_runs(self, num_runs = 1000000, play_optimally=True, player_hand=[], cards_to_remove=[]):

        if len(player_hand) != 0:
            print("Starting player hand: "+str(self.convert_cards(player_hand)))
        if len(cards_to_remove) != 0:
            print("Cards in other player's hand: {}".format(self.convert_cards(cards_to_remove)))


        self.reset()

        num_player_wins = 0
        num_dealer_wins = 0
        num_pushes = 0
        total_profit = 0

        for x in range(0, num_runs):

            starting_bankroll = self.bankroll

            winner = self.simulate_single(play_optimally, player_hand, cards_to_remove)

            #player wins with pair of jacks or better
            if winner == 1:
                num_player_wins += 1
                player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
                self.bankroll += sum(self.bets)*self.payout[player_hand_strength[0]]

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


        self.print_bankroll_state()

        print("Num player wins: {:,}".format(num_player_wins))
        print("Num dealer wins: {:,}".format(num_dealer_wins))
        print("Num pushes: {:,}".format(num_pushes))
        print("Win %: {:.2f}%".format(num_player_wins/num_runs*100))
        print("Lose %: {:.2f}%".format(num_dealer_wins/num_runs*100))
        print("Push %: {:.2f}%".format(num_pushes/num_runs*100))
        print("Avg return per hand: ${:,.2f}".format(total_profit/num_runs))
        print()
        self.print_hand_strength_distribution(num_runs)
        print()

        return num_player_wins, num_dealer_wins, num_pushes, total_profit, self.bankroll, copy.deepcopy(self.hand_strength_distribution)


    """
    Simulates a single game. Returns 1 if player wins, -1 if dealer wins, and 0 if push
    """
    def simulate_single(self, play_optimally=True, player_hand=None, cards_to_remove=[]):

        #shuffles the deck of cards
        self.initialize_deck()

        #make bets
        self.initial_bets()

        #player gets random cards
        if player_hand == None:
            self.player_hand[0] = self.deck.pop()
            self.player_hand[1] = self.deck.pop()

        #player gets certain cards
        self.player_hand = player_hand
        self.deck.pop(self.deck.index(self.player_hand[0]))
        self.deck.pop(self.deck.index(self.player_hand[1]))

        #Remove cards that you would see in other player's hands
        for card in cards_to_remove:
            try:
                #If type of card is wild, choose random card of that suit
                if "X" in card:
                    card = self.get_cards_same_suit(num_cards=1, suit=self.get_suit(card))[0]
                #If suit is wild, choose random card of that type
                elif "x" in card:
                    card = self.get_cards_same_type(num_cards=1, type=self.get_type(card))[0]

                self.deck.pop(self.deck.index(card))
            except Exception as error:
                print("Error: {}".format(error))
                pass

        #Shuffles since we removed cards from the bottom of the deck.
        random.shuffle(self.deck)


        #deal rest of cards
        self.deal()

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
    Given the suit of card (ex: h, s), randomly find the specified number of them
    """
    def get_cards_same_suit(self, num_cards, suit):
        cards = []
        for x in range(0, len(self.deck)):
            if self.get_suit(self.deck[x]) == suit:
                cards.append(self.deck[x])

            if len(cards) >= num_cards:
                break

        return cards

    """
    Given the type of card (ex: 13x), randomly find the specified number of them
    """
    def get_cards_same_type(self, num_cards, type):
        cards = []
        for x in range(0, len(self.deck)):
            if self.get_type(self.deck[x]) == type:
                cards.append(self.deck[x])

            if len(cards) >= num_cards:
                break

        return cards


    """
    Plays optimally according to wizard-of-odds

    Looking at player's hand, every street is bet in a way to simulate actual gameplay
    Ante is already bet
    """
    def play_optimally(self):

        if self.verbose:
            print("Player's hand: "+str(self.player_hand))
            print("Board: "+str(self.board))

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
            print("Board: "+str(self.board))

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
            print("Board: "+str(self.board))

        sorted_player_hand = sorted(self.player_hand)

        self.bet(1, self.bet_amount)
        self.bet(2, self.bet_amount)
        self.bet(3, self.bet_amount)
        

    """
    Basic strategy way to play 3rd street (1st community card)
    """
    def bet_3rd_street(self, sorted_player_hand):
        ###
        #bets 3rd street
        #To bet 3rd street, you can only see your cards, which is street="ante"
        # Strategy
        # - Raise 3x with any pair.
        # - Raise 1x with at least two points.
        # - Raise 1x with 6/5 suited.
        # Fold all others.

        bet_amount = 0

        points = self.get_num_points(street="ante")

        hand_strength = self.hand_strength.determine_hand_strength(board=[], hand=self.player_hand)

        #Raise 3x with any pair
        if hand_strength[0] == 1:
            bet_amount = self.bet_amount*3
        elif hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            bet_amount = self.bet_amount*3
        #raise 1x with at least 2 points
        elif points>=2:
            bet_amount = self.bet_amount
        #Raise 1x with 6/5 suited
        elif sorted_player_hand[0][0]==5 and sorted_player_hand[1][0]==6 and sorted_player_hand[0][1]==sorted_player_hand[1][1]:
            bet_amount = self.bet_amount
        else:
            self.fold = True
            return False

        # self.bets[1] = bet_amount
        self.bet(1, bet_amount)

        return True
    
    """
    Basic strategy way to play 4th street (2nd community card)
    """
    def bet_4th_street(self):
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

        bet_amount = 0

        points = self.get_num_points(street="3rd")

        hand_strength = self.hand_strength.determine_hand_strength(board=[self.board[0]], hand=self.player_hand)

        #Raise 3x with any made hand (mid pair or higher)
        if hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            bet_amount = self.bet_amount*3
        #Raise 1x with a low pair
        elif hand_strength[0]==1:
            bet_amount = self.bet_amount
        #raise 1x with at least 3 points
        elif points>=3:
            bet_amount = self.bet_amount
        #Raise 1x with any other three suited cards
        elif self.get_suit(self.player_hand[0])==self.get_suit(self.player_hand[1]) and self.get_suit(self.player_hand[1])==self.get_suit(self.board[0]):
            bet_amount = self.bet_amount
        #Fold all others
        else:
            self.fold = True
            return False

        self.bet(2, bet_amount)

        return True

    """
    Basic strategy way to play 5th street (3rd community card)
    """
    def bet_5th_street(self):
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

        bet_amount = 0

        points = self.get_num_points(street="4th")

        hand_strength = self.hand_strength.determine_hand_strength(board=self.board[0:2], hand=self.player_hand)

        
        #Raise 3x with any made hand (mid pair or higher)
        if hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
            bet_amount = self.bet_amount*3
        #Raise 3x with any four to a flush
        elif self.get_suit(self.player_hand[0])==self.get_suit(self.player_hand[1]) and \
            self.get_suit(self.player_hand[1])==self.get_suit(self.board[0]) and \
            self.get_suit(self.player_hand[1])==self.get_suit(self.board[1]):
            bet_amount = self.bet_amount*3
        #Raise 1x with a low pair
        elif hand_strength[0]==1:
            bet_amount = self.bet_amount
        #raise 1x with at least 4 points or Raise 1x with three mid cards and at least one previous 3x raise
        elif points>=4 or (points>=3 and self.bet_amount*3 in self.bets):
            bet_amount = self.bet_amount
        #Fold all others
        else:
            self.fold = True
            return

        self.bet(3, bet_amount)








    """
    Returns the number of "points" the player has. 
    Points are calculated according to wizard-of-odds. 


    High = J to A = 2 points
    Mid = 6 to 10 = 1 point
    Low = 2 to 5 = 0 points

    street values = ["ante", "3rd", "4th", "5th"]
    """
    def get_num_points(self, street="ante"):

        #only want points of player's hand
        if street == "ante":
            cards = self.player_hand

        #want points of player's hand and first card of board
        elif street == "3rd":
            cards = self.board[0:1] + self.player_hand

        #want points of player's hand and first two cards of board
        elif street == "4th":
            cards = self.board[0:2] + self.player_hand

        #want points of player's hand and first two cards of board
        elif street == "5th":
            cards = self.board + self.player_hand

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
    deals community cards and other player's cards

    board only has 3 cards in mississippi stud
    """
    def deal(self):
        self.board[0] = self.deck.pop()
        self.board[1] = self.deck.pop()
        self.board[2] = self.deck.pop()


    """
    prints current state of the board and bets
    """
    def print_current_state(self):
        self.print_bankroll_state()

        print("Ante bet: $"+str(self.bets[0]))
        print("3rd st bet: $"+str(self.bets[1]))
        print("4th st bet: $"+str(self.bets[2]))
        print("5th st bet: $"+str(self.bets[3]))

        self.print_board_state()

        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
        print("Player hand strength: {}".format(self.hand_strength.convert_hand_strength(player_hand_strength)))

        print()


    """
    Prints the state of the bankroll, like amount, bet size.
    """
    def print_bankroll_state(self):
        print()
        print("Starting bankroll: ${:,}".format(self.starting_bankroll))
        print("Bankroll: ${:,.2f}".format(self.bankroll))
        print("Bet size: ${:,}".format(self.bet_amount))
        print()
        

    """
    Prints the community cards and player hand
    """
    def print_board_state(self):
        print()
        print("Board: {},{},{}".format(self.convert_card(self.board[0]), self.convert_card(self.board[1]), self.convert_card(self.board[2])))
        print("player hand: {},{}".format(self.convert_card(self.player_hand[0]), self.convert_card(self.player_hand[1])))
        print()
        

    """
    Print distribution of each type of made hand, like % rates of pairs, two pairs, etc. 
    """
    def print_hand_strength_distribution(self, num_runs=None):
        #If don't specify number of runs, just print raw values
        if not num_runs:
            print(json.dumps(self.hand_strength_distribution, sort_keys=True, indent=4, default=str))
        #Print out rate that each hand type occurred
        else:
            new_hand_distribution = {}
            for key in self.hand_strength_distribution:
                new_hand_distribution[self.convert_hand_strength(key)] = "{:.2f}%".format(self.hand_strength_distribution[key]/num_runs*100)
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

        self.deck = deck

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


if __name__=="__main__":
    mississippi_stud = MississippiStud()
    mississippi_stud.run()