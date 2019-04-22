import CluedoUtils as cu

def main():
    print("CLUEDO")
    cg=cu.startGame(3)
    cg.revealSecret()
    gameOn=True
    currentPlayer=1
    while gameOn:
        print("Player "+str(currentPlayer)+":")
        print("make a move - will come here")

        # Now sort out a guess
        gs=cu.guess()
        if (currentPlayer==1):
            #it's you
            print("My hand:", cg.hands[0])
            print("My Score Card:")
            cg.gamecards[0].printme()
            gs.human_populate_guess()
        else:
            gs.computer_populate_guess(cg.gamecards[currentPlayer-1])

        # Now ask a question
        print("ask a question")
        cg.ask_question(gs,currentPlayer)
        gameOn=False

        gameOn=(input("Is Game Over Y/N)")=="N")

        currentPlayer=currentPlayer+1
        if (currentPlayer>3):
            currentPlayer=1

main()
