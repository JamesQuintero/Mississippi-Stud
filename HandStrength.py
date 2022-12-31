#
# Copyright (c) James Quintero 2020
#
# Last Modified: 12/2022
#

# Handles determining hand strength

class HandStrength:

    def __init__(self):
        self.verbose = False

    """
    returns 1 if hand1 won, -1 if hand2 won, and 0 if split
    """
    def determine_better_hand(self, hand1_strength, hand2_strength):

        if hand1_strength[0] > hand2_strength[0]:
            return 1
        elif hand1_strength[0] < hand2_strength[0]:
            return -1
        #if same hand
        else:
            #if returned hand data doesn't include lists
            if hand1_strength[0] == 8 or hand1_strength[0] == 5 or hand1_strength[0] == 4 or hand1_strength[0] == 9:
                if hand1_strength[1] > hand2_strength[1]:
                    return 1
                elif hand1_strength[1] < hand2_strength[1]:
                    return -1
                else:
                    return 0
            else:
                for x in range(0, len(hand1_strength[1])):
                    if hand1_strength[1][x] > hand2_strength[1][x]:
                        return 1
                    elif hand1_strength[1][x] < hand2_strength[1][x]:
                        return -1
                return 0

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
    Returns the hand strength along with kickers
    """
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

        has_straight = self.has_straight(cards)


        #if straight
        if has_straight[0] == True:
            str_height = has_straight[1]

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
        if has_straight[0] == True:
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




    """
    Gets indices for num_kickers
    """
    def get_kicker_indices(self, temp_cards, num_kickers):
        temp=[]
        for x in range(len(temp_cards)-1, -1, -1):
            if temp_cards[x]!=0 and len(temp)<num_kickers:
                temp.append(x)
        return temp


    """
    returns [True, straight_height] if has straight
    """
    def has_straight(self, cards):

        for x in range(2, len(cards)-4):
            if cards[x]>=1 and cards[x+1]>=1 and cards[x+2]>=1 and cards[x+3]>=1 and cards[x+4]>=1:
                return [True, x+4]

        #wheel straight
        if cards[2]>=1 and cards[3]>=1 and cards[4]>=1 and cards[5]>=1 and cards[14]>=1:
            return [True, 5]

        return [False, 0]


if __name__=="__main__":
    hand_strength = HandStrength()
    # mississippi_stud.run()