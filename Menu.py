#
# Copyright (c) James Quintero 2020
#
# Last Modified: 12/2022
#

#Menu provided to user for playing or simulating Mississippi Stud

from Play import Play
from Simulate import Simulate


class MississippiStud:

    def __init__(self):
        pass

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
        if choice == 1:
            play = Play()
            play.play()

        #simulate
        if choice == 2:
            self.simulate_menu()

        #print best strategy
        if choice == 3:
            print("Nothing here, yet")


    def simulate_menu(self):
        simulate = Simulate()

        print("Simulation menu: ")
        print("1) Simulate all cards")
        print("2) Simulate important cards (ex: KxAx is same as KxJx, 9x10 same as 9x6x, etc, so only simulate one)")
        print("3) Simulate flushes (Simulate flush possibilities while seeing other player's cards)")
        print("4) Simulate high cards (Player has two high cards and you see other player's hands)")

        choice = int(input("Choice: "))

        if choice == 1:
        # self.simulate()
            simulate.simulate_all_cards()
        elif choice == 2:
            simulate.simulate_important_cards()
        elif choice == 3:
            simulate.simulate_flushes()
        elif choice == 4:
            simulate.simulate_high_cards()



if __name__=="__main__":
    mississippi_stud = MississippiStud()
    mississippi_stud.run()