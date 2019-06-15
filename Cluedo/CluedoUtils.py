import random as rd
import csv

# Define immutable tuples for each of the game dimensions
rooms=('Hall','Lounge','Dining Room','Kitchen','Ballroom','Conservatory','Billiard Room','Library','Study')
people=('Miss Scarlet','Reverend Green','Mr Peacock','Mrs White','Professor Plum','Colonel Mustard')
weapons=('Dagger','Candlestick','Revolver','Rope','Lead Piping','Spanner')

# Re-arrange encoding to match the Cluedo Card Order.
MrsWhite=1
MissScarlet=2
RevGreen=3
MrPeacock=4
ProfPlum=5
ColMustard=6

#define the game dimensions. Look to remove boiler plate by having a guess consist of an array of game_dimensions
game_dimensions=('rooms','people','weapons')

class board:
    def __init__(self,filename):
       # self.boardData=[line.split(',') for line in open(filename)]

       with open(filename, newline="\n") as f:
            csvreader = csv.reader(f, delimiter=',')
            i=0
            for row in csvreader:
                if (i==0):
                    self.maxx=int(row[1])
                    self.maxy=int(row[2])
                    self.boardData = [[-1 for x in range(self.maxx+1)] for y in range(self.maxy+1)]
                else:
                    for c in range(len(row)):
                        self.boardData[c][i-1]=int(row[c])
                i=i+1

    def display(self):
        for y in range(self.maxy):
            lineStr=""
            for x in range(self.maxx):
                item=self.boardData[x][y]
               # print("x:",x+1," y+1:",y,"item:",item)
                if (item==-1): #Solid wall
                    lineStr=lineStr+"*"
                else:
                    if ((item & 3)==1 ):   #We're in a room
                        lineStr=lineStr+chr(ord("A")-1+((item & 60) >> 2))
                    if ((item & 3)==3):  #Door
                        lineStr=lineStr+"_"
                    if ((item & 3)==0):  #Passage
                        lineStr=lineStr+"."
                    if  ((item & 3)==2): # Start square
                        lineStr=lineStr+chr(ord("1")-1+((item & 28) >> 2))
            print("Row:"+str(y+1)+":"+lineStr)
            str1=""
            for i in range(self.maxx):
                str1=str1+str(self.boardData[i][y-1])+","
           #print(str1)

    def listNumbers(self):
        for y in range(self.maxy):
            lineStr = ""
            for x in range(self.maxx):
                print("x:",x+1,"y:",y+1,"item:",self.boardData[x][y])
                lineStr=lineStr+str(self.boardData[x][y])+","
          #  print("Row:" + str(y) + ":" + lineStr)


class guess:
    def __init__(self):
        self.room=""
        self.weapon=""
        self.person=""

    def human_populate_guess(self,thisScoreCard):

        for i in range (len(people)):
           personStr=people[i]
           if thisScoreCard.peopleMarks[personStr]!=False:
               print(i+1,".",personStr+"("+str(thisScoreCard.peopleMarks[personStr])+")")
           else:
            print(i+1,".",personStr)
        people_int=input("Pick a person [1.."+str(len(people))+"]")
        self.person=people[int(people_int)-1]

        for i in range (len(rooms)):
            #scard is a gamecard
            roomStr=rooms[i]
            if thisScoreCard.roomMarks[roomStr]!=False:
              print(i+1,".",roomStr+"("+str(thisScoreCard.roomMarks[roomStr])+")")
            else:
              print(i + 1, ".", roomStr)
        room_int=input("Pick a room [1.."+str(len(rooms))+"]")
        self.room=rooms[int(room_int)-1]

        for i in range (len(weapons)):
            weaponStr=weapons[i]
            if thisScoreCard.weaponMarks[weaponStr]!=False:
                print(i+1,".",weaponStr+"("+str(thisScoreCard.weaponMarks[weaponStr])+")")
            else:
                print(i+1,".",weaponStr)
        weapon_int=input("Pick a weapon [1.."+str(len(weapons))+"]")
        self.weapon=weapons[int(weapon_int)-1]
        print("guess:"+self.person+" "+self.weapon+" "+self.room)

    def computer_populate_guess(self,thisScoreCard):
        thisScoreCard.printme()
        remRooms=[r for r,b in thisScoreCard.roomMarks.items() if b==False]
        remPeople = [r for r, b in thisScoreCard.peopleMarks.items() if b == False]
        remWeapons= [r for r, b in thisScoreCard.weaponMarks.items() if b == False]
        # Pick a random from each and put them in case.
        self.room=rd.choice(remRooms)
        self.person = rd.choice(remPeople)
        self.weapon = rd.choice(remWeapons)

class scoreCard:
    def __init__(self):
        self.roomMarks=dict.fromkeys(rooms,False)
        self.weaponMarks=dict.fromkeys(weapons,False)
        self.peopleMarks=dict.fromkeys(people,False)

    def __init__(self,hand):
        self.roomMarks = dict.fromkeys(rooms, False)
        self.weaponMarks = dict.fromkeys(weapons, False)
        self.peopleMarks = dict.fromkeys(people, False)
        for i in range(len(hand)):
            #take each card and mark it True for everything in the player's hand
            card=hand[i]
            if card in rooms:
                dict.update(self.roomMarks,{card:True})
            if card in weapons:
                dict.update(self.weaponMarks,{card:True})
            if card in people:
                dict.update(self.peopleMarks,{card:True})

    def markScorecard(self, acard, playerNumber):
        if acard in rooms:
            dict.update(self.roomMarks,{acard:playerNumber})
        if acard in weapons:
            dict.update(self.weaponMarks,{acard:playerNumber})
        if acard in people:
            dict.update(self.peopleMarks,{acard:playerNumber})

    def printme(self):
        print(self.roomMarks)
        print(self.weaponMarks)
        print(self.peopleMarks)

class CluedoGame:
    def __init__(self,numPlayers):
        self.numPlayers=numPlayers
        # make a copy of the play lists that we can chop
        cpyRooms = list(rooms)
        cpyPeople = list(people)
        cpyWeapons = list(weapons)

        # take one card from each list, concatenate and then shuffle
        self.killer = cpyPeople.pop(rd.randint(0, len(cpyPeople) - 1))
        self.murder_room = cpyRooms.pop(rd.randint(0, len(cpyRooms) - 1))
        self.murder_weapon = cpyWeapons.pop(rd.randint(0, len(cpyWeapons) - 1))

        self.deck = cpyRooms + cpyPeople + cpyWeapons
        rd.shuffle(self.deck)

        #   divide up the cards between numPlayers
        self.hands = [[] for i in range(numPlayers)]
        player = 1
        while (len(self.deck) > 0):
            card = self.deck.pop(rd.randint(0, len(self.deck) - 1))
            self.hands[player - 1].append(card)
            player = player + 1
            if (player > numPlayers):
                player = 1

        # Set up gamecards for each player
        self.gamecards = []
        for i in range(numPlayers):
            self.gamecards.append(scoreCard(self.hands[i]))

        self.gameBoard=board("CluedoBoard.csv")

    def revealSecret(self):
        print("Top Secret:", self.killer, self.murder_room, self.murder_weapon)

    def ask_question(self, aGuess, playerNumber):
        print("guess from player"+str(playerNumber))
        print(aGuess.weapon+"-"+aGuess.person+"-"+aGuess.room)

        #start with next player
        checkPlayer=playerNumber+1
        if (checkPlayer>self.numPlayers):
                checkPlayer=1
        foundMatch=False
        while (foundMatch==False and checkPlayer!=playerNumber):
            print("checking hand vs player "+str(checkPlayer))

            #look at self.hands[checkPlayer] for any matches
            matches=[]
            for i in range(len(self.hands[checkPlayer-1])):
                thisCard=self.hands[checkPlayer-1][i-1]
                if (aGuess.person==thisCard):
                    matches.append(thisCard)
                if (aGuess.room == thisCard):
                    matches.append(thisCard)
                if (aGuess.weapon==thisCard):
                    matches.append(thisCard)

            if (len(matches)>0):
                foundMatch=True
                if (checkPlayer==1):
                    if (len(matches)==1):
                    # will need to prompt player which card to show - random for now#
                        showCard = rd.choice(matches)
                        print("You showed ",showCard," to player ",str(playerNumber))
                    else:
                        print("more than one card matches, which one would you like to show?")
                        for c in range(len(matches)):
                            print(c+1,".",matches[c])
                        choice=input("pick 1.."+str(c+1))
                        showCard=matches[int(choice)-1]
                else:
                    #pick a card at random to show
                    showCard=rd.choice(matches)

            else :
                checkPlayer = checkPlayer+1
                if (checkPlayer > self.numPlayers):
                    checkPlayer = 1

        #Mark the gameCard if there's a match
        if (foundMatch==True):
            print("found a match with player"+str(checkPlayer))
            #only show the card for player 1
            if (playerNumber==1):
                print(showCard)
            self.gamecards[playerNumber-1].markScorecard(showCard,checkPlayer)
            # Mark the card self.gamecards[playerNumber]
        else:
            print("no match found")
            #when no match found to knock out all the options if we didnt have the card
            if aGuess.person not in self.hands[playerNumber-1]:
                # mark everything other than aGuess.Person=True; Eventually change this to not overwrite info about what's in other players hands
                for  p in people:
                    if p!=aGuess.person and self.gamecards[playerNumber-1].peopleMarks[p]==False: #update every other person other than the guess person
                        dict.update(self.gamecards[playerNumber-1].peopleMarks, {p: "No Match"})
            if aGuess.weapon not in self.hands[playerNumber-1]:
                # mark everything other than aGuess.Person=True
                for  w in weapons:
                    if w!=aGuess.weapon and self.gamecards[playerNumber-1].weaponMarks[w]==False: #update every other weapon than than the guess weapon
                        dict.update(self.gamecards[playerNumber - 1].weaponMarks, {w: "No Match"})
            if aGuess.room not in self.hands[playerNumber-1]:
                # mark everything other than aGuess.Person=True
                for  r in rooms:
                    if r!=aGuess.room and self.gamecards[playerNumber-1].roomMarks[r]==False: #update every other  room apart from the guess room
                        dict.update(self.gamecards[playerNumber - 1].roomMarks, {r: "No Match"})
        return foundMatch

    def KnowAnswer(self, playerNum):
        # returns true if the current player has only one choice left on each card
        return ( len([r for r, b in self.gamecards[playerNum-1].roomMarks.items() if b == False])==1 and \
                 len([r for r, b in self.gamecards[playerNum-1].peopleMarks.items() if b == False])==1 and \
                 len ([r for r, b in self.gamecards[playerNum-1].weaponMarks.items() if b == False])==1)


    def GetAnswer(self, playerNum):
        # returns a guess object containing the answer if aPlayer has only one choice left in each category
        finalGuess: guess = guess()
        finalGuess.room=[r for r, b in self.gamecards[playerNum - 1].roomMarks.items() if b == False][0]
        finalGuess.person = [r for r, b in self.gamecards[playerNum - 1].peopleMarks.items() if b == False][0]
        finalGuess.weapon = [r for r, b in self.gamecards[playerNum - 1].weaponMarks.items() if b == False][0]
        return finalGuess


def startGame(numPlayers):
    assert numPlayers>1,"Must be more than 1 player"
    cg=CluedoGame(numPlayers)
    return cg


