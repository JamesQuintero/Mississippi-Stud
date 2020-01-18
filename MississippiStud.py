#
# Copyright (c) James Quintero 2020
#

#determines best strategy for playing Mississippi Stud

import os.path
import time
import sys
import random


class MississippiStud:

	#buy-in for $100
	bankroll = 100
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
		self.reset()
		self.board = [""]*3
		self.player_hand = [""]*2

		self.verbose = False

	def reset(self):
		# self.bankroll = 100
		self.bankroll = 1000000


	def run(self):

		print("Menu: ")
		print("1) Play")
		print("2) Simulate")
		print("3) Give best strategy")

		choice = int(input("Choice: "))


		#play
		if(choice==1):
			# play()
			print("Coming soon")



		#simulate
		if(choice==2):
			# print("Nothing here, yet")
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
				self.simulate(player_hands[x])
			# self.simulate([])

		#print best strategy
		if(choice==3):
			print("Nothing here, yet")


	"""
	simulates one game given the starting player_hand
	"""
	def simulate(self, player_hand=[]):

		if len(player_hand)!=0:
			print("Player hand: "+str(player_hand))


		self.reset()

		num_player_wins = 0
		num_dealer_wins = 0
		num_pushes = 0

		# num_runs=1
		num_runs = 1000000

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
			player_hand_strength = self.determine_hand_strength(self.board, self.player_hand)

			#1 if player won, 0 if push, -1 if player lost
			player_won = self.did_player_win(self.board, player_hand)



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
		self.print_current_state()


		print("Num player wins: "+str(num_player_wins))
		print("Num dealer wins: "+str(num_dealer_wins))
		print("Num pushes: "+str(num_pushes))

		print("Win %: "+str(num_player_wins/(num_player_wins+num_dealer_wins+num_pushes)))
		print("Lose %: "+str(num_dealer_wins/(num_player_wins+num_dealer_wins+num_pushes)))
		print("Push %: "+str(num_pushes/(num_player_wins+num_dealer_wins+num_pushes)))

		print()
		print()



	"""
	return 1 if player has won, 0 if player pushes, and -1 if player loses

	Player wins with a pair of jacks or better, pushes with a pair of 6s-10s, and loses all other times
	"""
	def did_player_win(self, board, player_hand):
		player_won = 0
		# #player won
		# if player_hand_strength[0]>1 or (player_hand_strength[0]==1 and player_hand_strength[1][0]>=11):
		# 	player_won = 1
		# #player pushed
		# elif player_hand_strength[0]==1 and player_hand_strength[1][0]>=6:
		# 	player_won = 0
		# #player lost
		# else:
		# 	player_won = -1

		return player_won


	"""
	returns 1 if hand1 won, 0 if hand2 won, and -1 if split
	"""
	def winner(self, hand1_strength, hand2_strength):

		if hand1_strength[0]>hand2_strength[0]:
			return 1
		elif hand1_strength[0]<hand2_strength[0]:
			return 0
		#if same hand
		else:
			#if returned hand data doesn't include lists
			if hand1_strength[0]==8 or hand1_strength[0]==5 or hand1_strength[0]==4 or hand1_strength[0]==9:
				if hand1_strength[1]>hand2_strength[1]:
					return 1
				elif hand1_strength[1]<hand2_strength[1]:
					return 0
				else:
					return -1
			else:
				for x in range(0, len(hand1_strength[1])):
					if hand1_strength[1][x]>hand2_strength[1][x]:
						return 1
					elif hand1_strength[1][x]<hand2_strength[1][x]:
						return 0
				return -1



	# #tests self.determine_hand_strength()
	# def test(self):

	# 	#tests flush
	# 	board=["12c", "11c", "10c", "5s", "3c"]
	# 	hand = ["14c", "13c"]

	# 	hand_strength = self.determine_hand_strength(board, hand)
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

		# self.bet(0, self.bet_amount)
		# self.bet(1, self.bet_amount*3)
		# self.bet(2, self.bet_amount*3)
		# self.bet(3, self.bet_amount*3)

		# return

		hand_strength = self.determine_hand_strength(board=[], hand=self.player_hand)


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
			return

		# self.bets[1] = bet_amount
		self.bet(1, bet_amount)




		###
		# bets 2nd street
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

		hand_strength = self.determine_hand_strength(board=[self.board[0]], hand=self.player_hand)

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
			return

		self.bet(2, bet_amount)



		###
		# bets 4 Cards (3rd street)
		# To bet 3rd street, you can only see your cards and the first two board cards, which is street="4th"
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

		hand_strength = self.determine_hand_strength(board=self.board[0:2], hand=self.player_hand)

		
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















		### For testing ###
		# self.bet(2, self.bets[1])
		# self.bet(3, self.bets[2])









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
		print()

		print("Bankroll: $"+str(self.bankroll))
		print("Bet size: $"+str(self.bet_amount))
		print()

		print("Ante bet: $"+str(self.bets[0]))
		print("3rd st bet: $"+str(self.bets[1]))
		print("4th st bet: $"+str(self.bets[2]))
		print("5th st bet: $"+str(self.bets[3]))
		print()

		# print("Dealer hand: "+self.convert_card(self.dealer_hand[0])+","+self.convert_card(self.dealer_hand[1]))
		print("Board: "+self.convert_card(self.board[0])+","+self.convert_card(self.board[1])+","+self.convert_card(self.board[2]))
		print("player hand: "+self.convert_card(self.player_hand[0])+","+self.convert_card(self.player_hand[1]))
		print()

		# dealer_hand_strength = self.determine_hand_strength(self.board, self.dealer_hand)
		# print("Dealer hand strength: "+str(dealer_hand_strength))

		player_hand_strength = self.determine_hand_strength(self.board, self.player_hand)
		print("Player hand strength: "+str(player_hand_strength))

		print()






	def determine_hand_strength(self, board, hand):
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

		#will return [#, [list of information like how high straight or flush is]]

		#starts at 0 spot (0 and 1 aren't used), and ends at Ace
		cards=[0]*15
		#spade, club, heart, diamond
		#list of cards that had that suit
		suits={"s": [], "c": [], "h": [], "d": []}

		#adds hand data to lists
		value1=int(hand[0][0:len(hand[0])-1])
		suit1=hand[0][-1:]
		value2=int(hand[1][0:len(hand[1])-1])
		suit2=hand[1][-1:]
		cards[value1]+=1
		suits[suit1].append(value1)
		cards[value2]+=1
		suits[suit2].append(value2)


		#adds board data to lists
		for x in range(0, len(board)):
			value=int(board[x][0:len(board[x])-1])
			suit=board[x][-1:]
			cards[value]+=1
			suits[suit].append(value)

		# print(hand)
		# print(board)
		# print(cards)
		# print(suits)

		has_straight=self.has_straight(cards)


		#if straight
		if has_straight[0]==True:
			str_height=has_straight[1]

			#if 5 of same suits in play and they're all in the straight
			for key in suits.keys():
				if len(suits[key])>=5 and str_height-4 in suits[key] and str_height-3 in suits[key] and str_height-2 in suits[key] and str_height-1 in suits[key] and str_height in suits[key]:
					
					#royal flush
					if str_height==14:
						return [9, 0]
					#straight flush
					return [8, str_height]

		#if quads
		if 4 in cards:
			quads=cards.index(4)

			#doesn't include quads in getting kicker
			cards[quads]=0

			#gets highest card in play
			kicker=self.get_kicker_indices(cards, 1)
			# kicker=kicker[0]

			extra = [quads]
			for x in range(0, min(1, len(kicker))):
				extra.append(kicker)

			return [7, extra]

		#if full house
		if (3 in cards and 2 in cards) or cards.count(3)==2:

			#gets highest 3 in play
			highest3=0
			for x in range(0, len(cards)):
				if cards[x]==3:
					highest3=x

			#doesn't include set of boat in getting other part
			cards[highest3]=0

			#gets highest 2 in play
			highest2=0
			for x in range(0, len(cards)):
				if cards[x]>=2:
					highest2=x

			#Aces of Kings full house will return [6, [14, 13]]
			return [6, [highest3, highest2]]

		#if flush
		for key in suits.keys():
			if len(suits[key])>=5:

				#returns highest player's flush if they have 2 of the suits
				if suit1==key and suit2==key:
					flush=max([value1, value2])
				#return player's flush if they have 1 of the suits or 0 if board plays
				if suit1==key:
					flush=value1
				elif suit2==key:
					flush=value2
				else:
					flush=0

				#returns highest card in flush
				return [5, flush]

		#if straight
		if has_straight[0]==True:
			return [4, has_straight[1]]

		#if trips
		if 3 in cards:
			trips=cards.index(3)

			#doesn't include trips in getting kicker
			cards[trips]=0

			#returns highest 2 cards not part of trips
			kickers=self.get_kicker_indices(cards, 2)
			extra = [trips]
			for x in range(0, min(2, len(kickers))):
				extra.append(kickers[x])

			return [3, extra]

		#if 2 pair
		if cards.count(2)>=2:
			#gets highest two pair
			highest1=0
			highest2=0
			for x in range(0, len(cards)):
				if cards[x]==2:
					highest2=highest1
					highest1=x

			#doesn't include 2 pair in getting kicker
			cards[highest1]=0
			cards[highest2]=0

			#gets high card
			kicker = self.get_kicker_indices(cards, 1)
			# kicker = kicker[0]
			extra = [highest1, highest2]

			for x in range(0, min(1, len(kicker))):
				extra.append(kicker[x])

			return [2, extra]

		#if regular pair
		if cards.count(2)==1:
			pair=cards.index(2)

			#doesn't include pair in getting kickers
			cards[pair]=0

			#get 3 other highest cards
			kickers=self.get_kicker_indices(cards, 3)

			values=[pair]
			for x in range(0, len(kickers)):
				if x<3:
					values.append(kickers[x])
			return [1, values]

		#if high card
		kickers=self.get_kicker_indices(cards, 5)
		return [0, kickers]




	#gets indicies for num_kickers
	def get_kicker_indices(self, temp_cards, num_kickers):
		temp=[]
		for x in range(len(temp_cards)-1, -1, -1):
			if temp_cards[x]!=0 and len(temp)<num_kickers:
				temp.append(x)
		return temp


	#returns [True, straight_height] if has straight
	def has_straight(self, cards):

		for x in range(2, len(cards)-4):
			if cards[x]>=1 and cards[x+1]>=1 and cards[x+2]>=1 and cards[x+3]>=1 and cards[x+4]>=1:
				return [True, x+4]

		#wheel straight
		if cards[2]>=1 and cards[3]>=1 and cards[4]>=1 and cards[5]>=1 and cards[14]>=1:
			return [True, 5]

		return [False, 0]


	def initialize_deck(self):

		#s = Spade
		#c = Club
		#h = Heart
		#d = Diamond
		deck=["2s","2c","2h","2d", 
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
		"14s","14c","14h","14d"]

		#creates randomized list of cards
		random_deck=[]
		while len(deck)!=0:

			#gets random index
			random_index=random.randint(0, len(deck)-1)
			random_deck.append(deck[random_index])
			deck.pop(random_index)

		self.deck = random_deck

	#turns 12s into Qs
	def convert_card(self, card):

		before=["2s","2c","2h","2d", 
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
		"14s","14c","14h","14d"]

		after=["2s","2c","2h","2d", 
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
		"As","Ac","Ah","Ad"]

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