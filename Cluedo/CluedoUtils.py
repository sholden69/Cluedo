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

def startGame(numPlayers):
    assert numPlayers>1,"Must be more than 1 player"

    #make a copy of the play lists that we can chop
    cpyRooms=rooms
    cpyPeople=people
    cpyWeapons=weapons

    # take one card from each list, concatenate and then shuffle
    killer=cpyPeople.pop(rd.randint(0,len(cpyPeople)-1))
    murder_room=cpyRooms.pop(rd.randint(0,len(cpyRooms)-1))
    murder_weapon=cpyWeapons.pop(rd.randint(0,len(cpyWeapons)-1))
    print("Top Secret:", killer, murder_room,murder_weapon)
    deck = cpyRooms + cpyPeople + cpyWeapons
    rd.shuffle(deck)

#   divide up the cards between numPlayers
    hands=[[] for i in range(numPlayers)]
    player=1
    while (len(deck)>0):
        card=deck.pop(rd.randint(0,len(deck)-1))
        hands[player-1].append(card)
        player=player+1
        if (player>numPlayers):
            player=1

   # Print my hand
    print("My hand:",hands[0])

# Assume that i will always be player 1
    gamecards=[]
    for i in range(numPlayers):
        gamecards.append(scoreCard(hands[i]))
    print("My Score Card:")
    gamecards[0].printme()