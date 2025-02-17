import random

class Deck:
    def __init__(self, game):
        if game == 'two_players':
            self.deck = ['Exploding Kitten'] * 1 + ['Attack'] * 2 +['Defuse'] * 3 + ['Cat Cards'] * 12 + ['Favor'] * 3 + ['Nope'] * 3 + ['See the Future'] * 3 + ['Shuffle'] * 2 + ['Skip'] * 3

        else:
            print("This game mode hasen't been developed yet")


    def shuffle(self):
        for i in range(len(self.deck) - 1):
            r = random.randint(i, len(self.deck) - 1)
            self.deck[i], self.deck[r] = self.deck[r], self.deck[i]


    def show_deck(self, n = -1):
        '''This function shows the first n cards of the deck. 
        If n = -1, then it shows all cards.'''
        if n == -1:
            print(self.deck)
        else:
            print([self.deck[i] for i in range(n)])


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.cards_number = []  #list of cards and number that represent their position in the
                                #list. Index starts from 1

    
    def show_cards(self):
        print(f'Your cards are \n{self.cards}\n')


class Table:
    #Table contains the discarded cards and the ones used to attack
    def __init__(self):
        self.cards = []
        self.attack_cards = []


class Match:
    def __init__(self, players, deck, table):
        '''
        This class represents a match.

        Input:
            players must be a list of players 

        Output:
            Each player will have a hand of cards
            '''
        self.players = players
        self.deck = deck
        self.table = table
        
        #extracting bombs
        bombs = []
        while 'Exploding Kitten' in self.deck.deck:
            bombs.append(self.deck.deck.pop(self.deck.deck.index('Exploding Kitten')))

        #extracting defusers
        defusers = []
        while 'Defuse' in self.deck.deck:
            defusers.append(self.deck.deck.pop(self.deck.deck.index('Defuse')))
        
        #giving one defuse to each player
        for player in self.players:
            card = defusers.pop()
            player.cards.append(card)
            player.cards_number.append((1,card))
        
        #put the defuser back in the deck
        while defusers:
            self.deck.deck.append(defusers.pop())

        #shuffle the deck
        self.deck.shuffle()

        for player in self.players:
            for i in range(7):
                card = self.deck.deck.pop()
                player.cards.append(card)
                player.cards_number.append((i+2, card))    #I need to use i+2 bcs there is already a diffuser in the player's cards
   
        #adding the bomb to the deck and shuffling again
        while bombs:
            self.deck.deck.append(bombs.pop())
        self.deck.shuffle()
        
        #it's used to assign the turn to the correct player
        self.player_turn = 0


    def turn(self):

        #choosing the right player for the turn
        player = self.players[self.player_turn]
        print('-'*100)
        print(f"It's {player.name}'s turn")
        self.player_turn = (self.player_turn + 1) % len(self.players)
        
        #checking if the previous player has used an attack card
        if self.table.attack_cards:
            print(f'Previous attack cards are {self.table.attack_cards}')
            attack_card = self.table.attack_cards.pop(-1)

            if attack_card == 'Attack':
                print(f'Do you want to use one of your cards? [y/n]\n\nYour cards are \n{player.cards}')
                answer = input()

                #checking that we have a valid input
                while answer not in ['y', 'n']:
                    print('You should enter a valid input')
                    print(f'Do you want to use one of your cards? [y/n]\n\nYour cards are \n{player.cards}')
                    answer = input()
                
                #Yes as answer. Use a card: update the player's cards and the table's cards
                if answer == 'y':
                    print(f'Which card do you want to use? [Reply with a number]\n\nYour cards are \n{player.cards_number}')
                    y = int(input())
                    used_card = player.cards.pop(y-1)
                    self.table.attack_cards.append(used_card)
                    print(f'Now your cards are \n{player.cards}')

                    print('Do you want to use another card? [y/n]')
                    answer = input()
                    while answer != 'n':
                        print(f'Which card do you want to use? [Reply with a number]\nYour cards are \n{player.cards_number}')
                        y = int(input())
                        used_card = player.cards.pop(y-1)
                        self.table.attack_cards.append(used_card)
                        print(f'Now your cards are \n{player.cards}')
                        print('Do you want to use another card? [y/n]')
                        answer = input()

                    return    #This player's turn is over

                else:    #Player doesn't use any of his cards
                    #take twice as many cards as the number of the attack cards
                    #I have to sum 1 bcs I've popped one 'Attack' card
                    n_attack = 1 + sum([1 for card in self.table.attack_cards if card == 'Attack'])
                    for _ in range(2*n_attack):
                        if self.deck.deck: #extracting a card from the deck and checking it
                            card = self.deck.deck.pop(0)
                            player.cards.append(card)
                            player.cards_number.append((len(player.cards), card))
                        else:
                            print('No more cards') #WHAT TO DO IF THERE AREN'T ANY MORE CARDS?'
                    self.table.cards.extend(self.table.attack_cards)   #add the attack cards to the table cards
                    self.table.attack_cards = []    #empty the list of attack cards

            else:    #here the attack card is 'Nope'
                print(f'Do you want to use one of your cards? [y/n]\nYour cards are {player.cards}')       #I could add the fact that you could just use another 'Nope'
                answer = input()
                while answer not in ['y', 'n']:
                    print('You should enter a valid input')
                    print(f'Do you want to use one of your cards? [y/n]\nYour cards are {player.cards}')
                    answer = input()

                if answer == 'y':
                    print(f'Which card do you want to use? [Reply with a number]\nYour cards are {player.cards_number}')
                    y = int(input())
                    used_card = player.cards.pop(y-1)
                    self.table.attack_cards.append(used_card)
                    print(f'Now your cards are {player.cards}')
                    return  #This player's turn is over

                else:
                    self.table.cards.extend(self.table.attack_cards)   #add the attack cards to the table cards
                    self.table.attack_cards = []    #empty the list of attack cards







        #if the previous player hasn't used any attack cards then the turn begins by asking if you want to extract a card or if you want to use one
        print(f'Your cards are\n{player.cards}\n\nDo you want to extract a card or do you want to use one of yours? The deck still has {len(self.deck.deck)} cards. [e/u]')
        choiche = input()
        while choiche not in ['e', 'u']:
            print('You should enter a valid input')
            print(f'Your cards are {player.cards}\n\nDo you want to extract a card or do you want to use one of yours? The deck still has {len(self.deck.deck)} cards [e/u]')
            choiche = input()

        if choiche == 'e':    #player chooses to extract a card
            if self.deck.deck: #extracting a card from the deck and checking it
                card = self.deck.deck.pop(0)
                print(f'The extracted card is {card}')
                player.cards.append(card)
                player.cards_number.append((len(player.cards_number), card))
            else:
                print('No more cards')

        else:    #player chooses to use a card
            print(f'Which card do you want to use? [Reply with a number]\n\nYour cards are {player.cards_number}')
            y = int(input())
            used_card = player.cards.pop(y-1)
            if used_card in ['Attack', 'Nope']:
                self.table.attack_cards.append(used_card)
                print(f'Now your cards are\n{player.cards}')
                return #This player's turn is over
            elif used_card in ['Favor', 'Cat Cards', 'See the Future', 'Shuffle', 'Skip']:
                print(f"You're using {used_card}")    #FINISH THIS!!! 
                #table.cards.append(used_cards)
                #should add the possibility to use multiple cards
                #must extract a card

        #Asking to show cards
        print('Do you want to see your cards? [y/n]')
        x = input()
        while x not in ['y', 'n']:
            print('Your answer must be in the form y or n')
            x = input()

        if x == 'y':
            player.show_cards()
        else:
            print('All right!')

        
        #If the player is at this point then it must discard a card
        print(f'Which card do you want to discard? [Reply with a number]\nYour cards are \n{player.cards_number}')
        y = int(input())
        player.cards.pop(y-1)
        print(f'Now your cards are \n{player.cards}')
        

