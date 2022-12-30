#
# Copyright (c) James Quintero 2020
#
# Last Modified: 12/2022
#

#determines best strategy for playing Mississippi Stud

import os.path
import time
import sys
import random

from HandStrength import HandStrength


class MississippiStud:

    hand_strength = None

    #Starting buy-in when sitting down at the table
    starting_bankroll = 1000
    #min-bet is $15
    bet_amount = 10
    #[0] = Ante bet, [1] = 3rd street bet, [2] = 4th street bet, [3] = 5th street bet
    bets = [0,0,0,0]
    fold = False

    deck = []
    board = []
    player_hand = []
    # dealer_hand = []




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

    def reset(self):
        # self.bankroll = 100
        self.bankroll = self.starting_bankroll


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
            num_runs = int(input("Num runs: "))

            player_hands = [
                ["14s", "14c"],
                # ["14s", "13c"],
                # ["14s", "12c"],
                # ["14s", "11c"],
                # ["14s", "10c"],
                # ["14s", "9c"],
                # ["14s", "8c"],
                # ["14s", "7c"],
                # ["14s", "6c"],
                # ["14s", "5c"],
                # ["14s", "4c"],
                # ["14s", "3c"],
                # ["14s", "2c"],

                # ["13s", "13c"],
                # ["13s", "12c"],
                # ["13s", "11c"],
                # ["13s", "10c"],
                # ["13s", "9c"],
                # ["13s", "8c"],
                # ["13s", "7c"],
                # ["13s", "6c"],
                # ["13s", "5c"],
                # ["13s", "4c"],
                # ["13s", "3c"],
                # ["13s", "2c"],

                # ["12s", "12c"],
                # ["12s", "11c"],
                # ["12s", "10c"],
                # ["12s", "9c"],
                # ["12s", "8c"],
                # ["12s", "7c"],
                # ["12s", "6c"],
                # ["12s", "5c"],
                # ["12s", "4c"],
                # ["12s", "3c"],
                # ["12s", "2c"],

                # ["11s", "11c"],
                # ["11s", "10c"],
                # ["11s", "9c"],
                # ["11s", "8c"],
                # ["11s", "7c"],
                # ["11s", "6c"],
                # ["11s", "5c"],
                # ["11s", "4c"],
                # ["11s", "3c"],
                # ["11s", "2c"],

                # ["10s", "10c"],
                # ["10s", "9c"],
                # ["10s", "8c"],
                # ["10s", "7c"],
                # ["10s", "6c"],
                # ["10s", "5c"],
                # ["10s", "4c"],
                # ["10s", "3c"],
                # ["10s", "2c"],

                # ["9s", "9c"],
                # ["9s", "8c"],
                # ["9s", "7c"],
                # ["9s", "6c"],
                # ["9s", "5c"],
                # ["9s", "4c"],
                # ["9s", "3c"],
                # ["9s", "2c"],

                # ["8s", "8c"],
                # ["8s", "7c"],
                # ["8s", "6c"],
                # ["8s", "5c"],
                # ["8s", "4c"],
                # ["8s", "3c"],
                # ["8s", "2c"],

                # ["7s", "7c"],
                # ["7s", "6c"],
                # ["7s", "5c"],
                # ["7s", "4c"],
                # ["7s", "3c"],
                # ["7s", "2c"],

                # ["6s", "6c"],
                # ["6s", "5c"],
                # ["6s", "4c"],
                # ["6s", "3c"],
                # ["6s", "2c"],

                # ["5s", "5c"],
                # ["5s", "4c"],
                # ["5s", "3c"],
                # ["5s", "2c"],

                # ["4s", "4c"],
                # ["4s", "3c"],
                # ["4s", "2c"],

                # ["3s", "3c"],
                # ["3s", "2c"]
            ]

            for x in range(0, len(player_hands)):
                self.simulate(num_runs, player_hands[x])

        #print best strategy
        if(choice==3):
            print("Nothing here, yet")


    """
    simulates one game given the starting player_hand
    """
    def simulate(self, num_runs = 1000000, player_hand=[]):

        if len(player_hand)!=0:
            print("Starting player hand: "+str(self.convert_cards(player_hand)))


        self.reset()

        num_player_wins = 0
        num_dealer_wins = 0
        num_pushes = 0

        # while(True):
        for x in range(0, num_runs):

            #shuffles the deck of cards
            self.initialize_deck()

            #make bets
            self.initial_bets()

            
            # #player gets random cards
            # self.player_hand[0] = self.deck.pop()
            # self.player_hand[1] = self.deck.pop()

            #player gets certain cards
            self.player_hand = player_hand
            self.deck.pop(self.deck.index(self.player_hand[0]))
            self.deck.pop(self.deck.index(self.player_hand[1]))



            #if you saw that another player has an ace
            self.deck.pop(self.deck.index("14h"))


            #deal rest of cards
            self.deal()

            # #player bets 4x
            # self.bets[3] = self.bet*4
            # self.bankroll -= self.bets[3]


            #player bets optimally, according to wizard-of-odds
            self.play_optimally()



            #if player folded, just skip to the next hand
            if self.fold:
                num_dealer_wins += 1
                continue 



            # dealer_hand_strength = self.determine_hand_strength(self.board, self.dealer_hand)
            player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)

            #player wins with pair of jacks or better
            if player_hand_strength[0] >= 2 or (player_hand_strength[0] == 1 and player_hand_strength[1][0]>=11):
                num_player_wins += 1
                self.bankroll += sum(self.bets)*self.payout[player_hand_strength[0]]

            #pushes with pair of 6s to pair of 10s
            elif player_hand_strength[0] == 1 and player_hand_strength[1][0]>=6:
                num_pushes += 1
                self.bankroll += sum(self.bets)

            #player lost
            else:
                num_dealer_wins += 1




            if x!=0 and x%100000 == 0:
                print("Hand #"+str(x))



        # print("Player hand: "+str(player_hand))
        self.print_bankroll_state()


        print("Num player wins: "+str(num_player_wins))
        print("Num dealer wins: "+str(num_dealer_wins))
        print("Num pushes: "+str(num_pushes))

        print("Win %: "+str(num_player_wins/(num_player_wins+num_dealer_wins+num_pushes)*100))
        print("Lose %: "+str(num_dealer_wins/(num_player_wins+num_dealer_wins+num_pushes)*100))
        print("Push %: "+str(num_pushes/(num_player_wins+num_dealer_wins+num_pushes)*100))

        print()
        print()



    # def test(self):

    # 	#tests flush
    # 	board=["12c", "11c", "10c", "5s", "3c"]
    # 	hand = ["14c", "13c"]

    # 	hand_strength = self.hand_strength.determine_hand_strength(board, hand)
    # 	print(hand_strength)



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





        ### For testing ###
        # self.bet(2, self.bets[1])
        # self.bet(3, self.bets[2])
        

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
        # if hand_strength[0]==1:
        # 	bet_amount = self.bet_amount*3
        if hand_strength[0] >= 2 or (hand_strength[0]==1 and hand_strength[1][0]>=6):
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


        # print("Cards: "+str(cards))


        #gets points of all cards
        points = 0
        for card in cards:
            value = int(card[:-1])
            suit = card[1]

            # print("Value: "+str(value))

            #J-A are 2 points
            if value >= 11:
                points += 2
            #6-10 are 1 point
            elif value >= 6:
                points += 1
            #2-5 are 0 points
            else:
                points += 0




        # print("Points: "+str(points))
        # input()
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
    """
    def deal(self):

        #board only has 3 cards in mississippi stud
        self.board[0] = self.deck.pop()
        self.board[1] = self.deck.pop()
        self.board[2] = self.deck.pop()
        # self.board[3] = self.deck.pop()
        # self.board[4] = self.deck.pop()




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

        # dealer_hand_strength = self.determine_hand_strength(self.board, self.dealer_hand)
        # print("Dealer hand strength: "+str(dealer_hand_strength))

        player_hand_strength = self.hand_strength.determine_hand_strength(self.board, self.player_hand)
        print("Player hand strength: {}".format(self.hand_strength.convert_hand_strength(player_hand_strength)))

        print()


    """
    Prints the state of the bankroll, like amount, bet size.
    """
    def print_bankroll_state(self):
        print()
        print("Starting bankroll: ${:,}".format(self.starting_bankroll))
        print("Bankroll: ${:,}".format(self.bankroll))
        print("Bet size: ${:,}".format(self.bet_amount))
        print()
        

    def print_board_state(self):
        print()
        # print("Dealer hand: "+self.convert_card(self.dealer_hand[0])+","+self.convert_card(self.dealer_hand[1]))
        print("Board: {},{},{}".format(self.convert_card(self.board[0]), self.convert_card(self.board[1]), self.convert_card(self.board[2])))
        print("player hand: {},{}".format(self.convert_card(self.player_hand[0]), self.convert_card(self.player_hand[1])))
        print()


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

        return to_return[hand_strength[0]]

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


    def convert_cards(self, cards):
        to_return = []
        for x in range(0, len(cards)):
            to_return.append(self.convert_card(cards[x]))
        return to_return

    """
    Turns 12s into Qs
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

    #gets the suit from the card
    def get_suit(self, card):
        return card[-1:]


    #converts 25.000000000000000001 to 25.0
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