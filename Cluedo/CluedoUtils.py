import random as rd

rooms=['Hall','Lounge','Dining Room','Kitchen','Ballroom','Conservatory','Billiard Room','Library','Study']
people=['Miss Scarlet','Reverend Green','Mr Peacock','Mrs White','Professor Plum','Colonel Mustard']
weapons=['Dagger','Candlestick','Revolver','Rope','Lead Piping','Spanner']

class guess:
    def __init__(self):
        self.room=""
        self.weapon=""
        self.person=""

    def human_populate_guess(self,thisScoreCard):
        for i in range (len(rooms)):
            #scard is a gamecard
            roomStr=rooms[i]
            if thisScoreCard.roomMarks[roomStr]==True:
              print(i+1,".",roomStr+"(Y)")
            else:
              print(i + 1, ".", roomStr)
        room_int=input("Pick a room [1.."+str(len(rooms))+"]")
        self.room=rooms[int(room_int)-1]

        for i in range (len(people)):
           personStr=people[i]
           if thisScoreCard.peopleMarks[personStr]==True:
               print(i+1,".",personStr+"(Y)")
           else:
            print(i+1,".",personStr)
        people_int=input("Pick a person [1.."+str(len(rooms))+"]")
        self.person=people[int(people_int)-1]


        for i in range (len(weapons)):
            weaponStr=weapons[i]
            if thisScoreCard.weaponMarks[weaponStr]==True:
                print(i+1,".",weaponStr+"(Y)")
            else:
                print(i+1,".",weaponStr)
        weapon_int=input("Pick a weapon [1.."+str(len(rooms))+"]")
        self.weapon=weapons[int(weapon_int)-1]
        print("guess:"+self.person+" "+self.weapon+" "+self.room)

    def computer_populate_guess(self,thisScoreCard):
        print("Building computer guess...")
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
            #take each card and mark it
            card=hand[i]
            if card in rooms:
                dict.update(self.roomMarks,{card:True})
            if card in weapons:
                dict.update(self.weaponMarks,{card:True})
            if card in people:
                dict.update(self.peopleMarks,{card:True})

    def markScorecard(self, acard):
        if acard in rooms:
            dict.update(self.roomMarks,{acard:True})
        if acard in weapons:
            dict.update(self.weaponMarks,{acard:True})
        if acard in people:
            dict.update(self.peopleMarks,{acard:True})

    def printme(self):
        print("Score Card:")
        print(self.roomMarks)
        print(self.weaponMarks)
        print(self.peopleMarks)

class CluedoGame:
    def __init__(self,numPlayers):
        self.numPlayers=numPlayers
        # make a copy of the play lists that we can chop
        cpyRooms = rooms
        cpyPeople = people
        cpyWeapons = weapons

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
                for i in range(len(matches)):
                    print(matches[i-1])

                if (checkPlayer==1):
                    print("will need to prompt player which card to show - random for now")
                    showCard = rd.choice(matches)
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
            self.gamecards[playerNumber-1].markScorecard(showCard)
            # Mark the card self.gamecards[playerNumber]
        else:
            print("no match found")
        return foundMatch

    def KnowAnswer(self, aPlayer):
        print("returns true if the current player has only one choice left on each card")
        return False

    def GetAnswer(self, aPlayer):
        print("returns a guess object containing the answer if aPlayer has only one choice left in each category")
        finalGuess: guess = guess()
        return finalGuess


def startGame(numPlayers):
    assert numPlayers>1,"Must be more than 1 player"
    cg=CluedoGame(numPlayers)
    return cg


