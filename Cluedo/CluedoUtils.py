import random as rd

rooms=['Hall','Lounge','Dining Room','Kitchen','Ballroom','Conservatory','Billiard Room','Library','Study']
people=['Miss Scarlet','Reverend Green','Mr Peacock','Mrs White','Professor Plum','Colonel Mustard']
weapons=['Dagger','Candlestick','Revolver','Rope','Lead Piping','Spanner']

class guess:
    def __init__(self):
        self.room=""
        self.weapon=""
        self.person=""

    def human_populate_guess(self):
        for i in range (len(rooms)):
            print(i+1,".",rooms[i])
        room_int=input("Pick a room [1.."+str(len(rooms))+"]")
        self.room=rooms[int(room_int)-1]
        for i in range (len(people)):
            print(i+1,".",people[i])
        people_int=input("Pick a person [1.."+str(len(rooms))+"]")
        self.person=people[int(people_int)-1]
        for i in range (len(weapons)):
            print(i+1,".",weapons[i])
        weapon_int=input("Pick a weapon [1.."+str(len(rooms))+"]")
        self.weapon=weapons[int(weapon_int)-1]
        print("guess:"+self.person+" "+self.weapon+" "+self.room)

    def computer_populate_guess(self,thisScoreCard):
        print("Building computer guess...")
        thisScoreCard.printme()
        remRooms={r:b for r,b in thisScoreCard.roomMarks.items() if b==False}
        remPeople = {r: b for r, b in thisScoreCard.roomPeople.items() if b == False}
        remWeapons= {r: b for r, b in thisScoreCard.roomWeapons.items() if b == False}
        # Pick a random from each and put them in case.
        return

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


    def printme(self):
        print("Card Status:")
        print(self.roomMarks)
        print(self.weaponMarks)
        print(self.peopleMarks)

class CluedoGame:
    def __init__(self,numPlayers):
        self.test=""
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
        print("asking a question")
        return

def startGame(numPlayers):
    assert numPlayers>1,"Must be more than 1 player"

    cg=CluedoGame(numPlayers)
    return cg


