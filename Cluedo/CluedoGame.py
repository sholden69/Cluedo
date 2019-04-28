import CluedoUtils as cu

def main():
    numPlayers=3
    print("CLUEDO")
    cg=cu.startGame(numPlayers)
    gameOn=True
    currentPlayer=1
    while gameOn:
        print("********* Player "+str(currentPlayer)+"***************")
        cg.revealSecret()
        if cg.KnowAnswer(currentPlayer):
            print("move to the middle to win the game with")
            finalAnswer = cg.GetAnswer(currentPlayer)
            print(finalAnswer.person, " in", finalAnswer.room, " with ", finalAnswer.weapon)
            gameOn = False
            exit(0)

        print("make a move - will come here")

        # Now sort out a guess
        gs=cu.guess()
        if (currentPlayer==1):
            #it's you
            print("My hand:", cg.hands[0])
            cg.gamecards[0].printme()
            gs.human_populate_guess(cg.gamecards[0])
        else:
            gs.computer_populate_guess(cg.gamecards[currentPlayer-1])

        # Now ask a question

        cg.ask_question(gs,currentPlayer)

        #Check to continue after human player go
        if currentPlayer==1:
            gameOn=(input("Is Game Over Y/N)")=="N")

        # Move on to the next player
        currentPlayer=currentPlayer+1
        if (currentPlayer>numPlayers):
            currentPlayer=1

main()
