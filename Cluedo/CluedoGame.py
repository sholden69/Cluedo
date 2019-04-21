import CluedoUtils as cu

def main():
    print("CLUEDO")
    cg=cu.startGame(3)
    cg.revealSecret()
    gameOn=True
    while gameOn:
        print("My hand:", cg.hands[0])
        print("My Score Card:")
        cg.gamecards[0].printme()
        print("make a move")
        print("ask a question")
        gs=cu.guess()
        gs.human_populate_guess()
        cg.ask_question(gs)
        gameOn=False

main()
