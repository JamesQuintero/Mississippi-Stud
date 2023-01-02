

## Pair stats
* Given a high pair, like KxKx, there's a 100% chance you win. Makes around 15x bet per hand. This is more than the 9x bet max you can put out, and that's due to getting trips, two pair, etc. 
* Given a middle pair, like 8x8x, there's a 30% chance you win and a 70% chance you push. Make around 8x bet per hand. 
* Given a low pair, like 5x5x, there's a 30% chance you win, a 70% chance you lose, and 0% chance of pushing. Make around 0.4x per hand. 

## Hand strengths probability for any pair
Given any pair, there's a 72% chance of getting a pair, 16% chance of two pair, 10% chance of trips, and 1% chance of full house. Quads are 1/4th the chance as a full house, so around 0.25%. 

## High cards stats
* Given two high cards, like KxQx, there's a 35% chance you win, 60% chance you lose, and 5% chance you push. 
  * This is the same whether the cards are suited or not. 
  * However, unsuited high cards return around 0.5x ante bet, while suited high cards return around 1x ante bet. 
    * This is entirely from flushes, straight flushes, and royal flushes.
  * ~50% chance only end up with a high card and lose max bets. 
  * 35% chance end up with a pair and push/win, 4% chance of getting two pair, 1.5% chance of trips, 0.6% chance of straight, and 1% chance of full house. 
    * This barely changes when the two high cards are suited. Flushes have around 0.8% chance, and straight/royal flushes around 1/20,000
* 

## One High One Push card stats
* Given a high card and a medium card, like Kx9x, there's a 23% chance you win, 58% chance you lose, and 18% chance you push. 
  * The chance of losing is the same as two high cards, but the chance of pushing is significantly higher. 
* 



## Flush cards taken
* No matter the cards, if they are suited, there's a 0.83% chance of getting a flush. If you see the following amount of suits in other player's hands, this is how those odds change
* The following is if player's hand is two low cards. 
* Profitability doesn't decrease significantly if player sees other player's have the same suit as them.
* Profitrability increases as player sees other players don't have the correct suit, but only slightly. 

| # Other player's cards | Win % | Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % | Straight Flush %
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0 cards | 0.12 | -$20.19 | 11.0524 | 4.0207 | 1.5523 | 1.3002 | 0.8411 | 0.0991 | 0.0097 | 0.0143
| 1 suit match | 0.12 | -$20.05 | 11.0349 | 4.0208 | 1.5739 | 1.2915 | 0.8367 | 0.094 | 0.0113 | 0.0171
| 3 suit match | 0.12 | -$20.13 | 11.0392 | 4.0373 | 1.5674 | 1.2972 | 0.8316 | 0.0981 | 0.01 | 0.0149
| 6 suit match | 0.12 | -$20.22 | 10.9872 | 4.0695 | 1.5643 | 1.2966 | 0.8118 | 0.0882 | 0.0109 | 0.0153
| 1 suit different | 0.12 | -$19.85 | 10.7758 | 4.1473 | 1.6154 | 1.3728 | 0.8771 | 0.0993 | 0.0097 | 0.0171
| 3 suit different | 0.13 | -$18.61 | 10.3242 | 4.3932 | 1.7232 | 1.5483 | 0.9839 | 0.1124 | 0.0127 | 0.0185
| 6 suit different | 0.14 | -$17.14 | 9.6312 | 4.8041 | 1.9337 | 1.5268 | 1.2397 | 0.1349 | 0.0174 | 0.0215
| 8 suit different | 0.15 | -$16.67 | 9.5851 | 5.0746 | 2.0791 | 1.0982 | 1.4189 | 0.1617 | 0.0153 | 0.0229
| 10 suit different | 0.15 | -$14.91 | 9.9164 | 5.374 | 2.2183 | 1.1053 | 1.634 | 0.187 | 0.0183 | 0.0305



## Winning cards taken
How do your odds change if you see other players do or do not have either of your high cards? 

* If other players have 3 of one of your high cards, it is unprofitable to play. 
* If player has 2 high cards, and they see 4+ other players do not have any of those high cards, they should raise 3x for 3rd street. 

| Player's hand | # Other player's cards | Win % | Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 2 high cards |  | 0.35 | 4.93 | 35.417 | 3.967 | 1.58 | 0.606 | 0 | 0.105 | 0.011 | 0 | 0 |
| 2 high cards | 1 matching | 0.31 | -0.75 | 32.844 | 3.262 | 1.174 | 0.672 | 0 | 0.051 | 0.007 | 0 | 0 |
| 2 high cards | 2 matching | 0.27 | -6.03 | 30.066 | 2.288 | 1.006 | 0.767 | 0 | 0.013 | 0.011 | 0 | 0 |
| 2 high cards | 3 matching | 0.22 | -11.51 | 26.852 | 1.212 | 1.088 | 0.79 | 0 | 0 | 0.005 | 0 | 0 |
| 2 high cards | 1 different | 0.36 | 6.26 | 36.318 | 4.076 | 1.644 | 0.738 | 0 | 0.107 | 0.01 | 0 | 0 |
| 2 high cards | 3 different | 0.37 | 7.99 | 37.061 | 4.412 | 1.743 | 0.736 | 0 | 0.132 | 0.011 | 0 | 0 |
| 2 high cards | 6 different | 0.38 | 9.93 | 38.254 | 4.749 | 1.888 | 0.452 | 0 | 0.15 | 0.018 | 0 | 0 |
| 2 high cards | 8 different | 0.39 | 11.43 | 38.851 | 5.07 | 2.097 | 0.433 | 0 | 0.155 | 0.008 | 0 | 0 |
| 2 high cards | 10 different | 0.41 | 14.15 | 38.997 | 5.369 | 2.285 | 0.517 | 0 | 0.206 | 0.013 | 0 | 0 |
| 1 high 1 low |  | 0.18 | -9.16 | 18.83 | 3.416 | 1.375 | 0 | 0 | 0.077 | 0.013 | 0 | 0 |
| 1 high 1 low | 1 matching | 0.14 | -14.58 | 15.872 | 2.739 | 1.039 | 0 | 0 | 0.059 | 0.003 | 0 | 0 |
| 1 high 1 low | 2 matching | 0.1 | -19.46 | 13.315 | 1.965 | 0.863 | 0 | 0 | 0.014 | 0.008 | 0 | 0 |
| 1 high 1 low | 3 matching | 0.06 | -24.74 | 9.828 | 1.012 | 0.934 | 0 | 0 | 0 | 0.003 | 0 | 0 |
| 1 high 1 low | 1 different | 0.18 | -9.89 | 19.697 | 2.804 | 1.077 | 0 | 0 | 0.047 | 0.007 | 0 | 0 |
| 1 high 1 low | 3 different | 0.18 | -9.24 | 20.327 | 2.983 | 1.131 | 0 | 0 | 0.063 | 0.004 | 0 | 0 |
| 1 high 1 low | 6 different | 0.19 | -8.33 | 21.054 | 3.15 | 1.207 | 0 | 0 | 0.056 | 0.007 | 0 | 0 |
| 1 high 1 low | 8 different | 0.2 | -7.07 | 21.744 | 3.386 | 1.323 | 0 | 0 | 0.065 | 0.009 | 0 | 0 |
| 1 high 1 low | 10 different | 0.22 | -5.49 | 21.533 | 3.608 | 1.483 | 0 | 0 | 0.073 | 0.015 | 0 | 0 |


## Middle cards taken
* Played optimally  
* If even two of the middle cards match in another player's hand, fold. 

| # Other player's cards | Win % | Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0 | 0.09 | -$8.84 | 26.531 | 3.266 | 1.327 | 0.323 | 0 | 0.094 | 0.012 |
| 1 match | 0.08 | -$11.87 | 24.835 | 2.709 | 0.968 | 0.345 | 0 | 0.048 | 0.005 |
| 2 same match | 0.07 | -$14.73 | 22.72 | 1.729 | 0.828 | 0.359 | 0 | 0.012 | 0.007 |
| 3 match | 0.07 | -$16.91 | 20.179 | 0.937 | 0.856 | 0.403 | 0 | 0 | 0.005 |
| 1 of each match | 0.08 | -$14.78 | 22.59 | 2.046 | 0.63 | 0.37 | 0 | 0.035 | 0 |
| 2 of each match | 0.07 | -$19.67 | 17.325 | 0.919 | 0.186 | 0.409 | 0 | 0 | 0 |
| 1 different | 0.09 | -$8.07 | 27.525 | 3.477 | 1.395 | 0.346 | 0 | 0.105 | 0.011 |
| 3 different | 0.1 | -$6.98 | 27.875 | 3.777 | 1.511 | 0.394 | 0 | 0.122 | 0.01 |
| 6 different | 0.09 | -$5.84 | 28.768 | 3.974 | 1.66 | 0.52 | 0 | 0.129 | 0.016 |
| 8 different | 0.1 | -$4.46 | 29.327 | 4.328 | 1.774 | 0.429 | 0 | 0.169 | 0.019 |
| 10 differenmt | 0.11 | -$3.56 | 29.21 | 4.392 | 1.895 | 0.299 | 0 | 0.184 | 0.025 |



## Losing cards taken
* Played to the end, since optimal play says to always fold these hands.
* No matter number of non-matching cards in other player's hands, not profitable to play 2 losing cards.

| # Other player's cards | Win % | Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
|  | 0.11 | -24.39 | 11.0494 | 4.029 | 1.567 | 0.6485 | 0 | 0.0905 | 0.0114 |
| 1 different | 0.11 | -24.18 | 11.4055 | 4.1395 | 1.6323 | 0.5203 | 0 | 0.1016 | 0.0097 |
| 3 different | 0.11 | -23.91 | 11.7286 | 4.3923 | 1.7476 | 0.354 | 0 | 0.1087 | 0.0128 |
| 6 different | 0.11 | -23.41 | 11.6322 | 4.8124 | 1.9376 | 0.3161 | 0 | 0.1422 | 0.014 |
| 8 different | 0.11 | -22.85 | 11.0063 | 5.0784 | 2.09 | 0.3144 | 0 | 0.1558 | 0.0179 |
| 10 different | 0.12 | -22.24 | 10.2166 | 5.3493 | 2.1959 | 0.3701 | 0 | 0.1814 | 0.0208 |




## Middle cards not taken
Seems that no matter what cards the player is holding, if they see other player's cards do not match the player's cards, their chance of winning goes up significantly. 
* If the player has middle cards, like 10x9x, their chance of winning goes up slowly the more high cards they see in other player's hands. But only because it means there are fewer non-pair cards for community cards. 
  * You would think the more winning cards that are taken up by players would reduce the player's chance of winning because it lowers the chance the board will pair, but that's overshadowed by the increase in chance the player pairs their own cards. 
  * The win % goes down as other players have more high cards, but the avg profit goes up due to the player's increased chance of getting good hands. 

| # Other player's cards | Win % |  Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0 | 0.12 | -$13.23 | 35.5257 | 4.0337 | 1.5944 | 1.3062 | 0 | 0.0911 | 0.011 |
| 2 | 0.11 | -$13.5 | 35.6656 | 4.1489 | 1.6204 | 1.1256 | 0 | 0.0962 | 0.0113 |
| 3 | 0.11 | -$13.17| 35.783 | 4.3713 | 1.7285 | 1.2125 | 0 | 0.1106 | 0.0121 |
| 6 | 0.1 | -$12.66 | 36.2831 | 4.875 | 1.9622 | 1.0605 | 0 | 0.1355 | 0.0164 |
| 8 | 0.09 | -$12.02 | 36.6836 | 5.255 | 2.1088 | 1.0669 | 0 | 0.1602 | 0.0182 |
| 10 | 0.1 | -$11.02 | 37.4605 | 5.8087 | 2.3573 | 0.9393 | 0 | 0.1787 | 0.0198 |

* If the player has middle cards, like 10x9x, their chance of winning goes up significantly the more low cards they see in other player's hands. 

| # Other player's cards | Win % | Avg profit $ | Pair % | Two Pair % | Trips % | Straight % | Flush % | Full House % | Quads % |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0 | 0.12 | -$13.28 | 35.5496 | 4.0381 | 1.5669 | 1.2932 | 0 | 0.0969 | 0.0099 |
| 1 | 0.12 | -$12.49 | 36.1799 | 4.1451 | 1.6326 | 1.3836 | 0 | 0.0996 | 0.0122 |
| 3 | 0.13 | -$10.7 | 37.7557 | 4.404 | 1.7344 | 1.596 | 0 | 0.1156 | 0.0156 |
| 6 | 0.15 | -$7.72 | 40.3725 | 4.8472 | 1.9702 | 1.9231 | 0 | 0.1349 | 0.0157 |
| 8 | 0.16 | -$5.18 | 42.2325 | 5.2584 | 2.1593 | 2.2228 | 0 | 0.16 | 0.0196 |
| 10 | 0.18 | -$2.35 | 44.1054 | 5.8144 | 2.3321 | 2.6127 | 0 | 0.185 | 0.0207 |
