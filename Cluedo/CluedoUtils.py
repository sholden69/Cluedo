import random as rd

rooms=['Hall','Lounge','Dining Room','Kitchen','Ballroom','Conservatory','Billiard Room','Library','Study']
people=['Miss Scarlet','Reverend Green','Mr Peacock','Mrs White','Professor Plum','Colonel Mustard']
weapons=['Dagger','Candlestick','Revolver','Rope','Lead Piping','Spanner']


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

def startGame(numPlayers):
    assert numPlayers>1,"Must be more than 1 player"

    cg=CluedoGame(numPlayers)
    return cg

def guess():
#given a room + weapon + person, returns false if no player has any else the player number and card
    print ("guess")
