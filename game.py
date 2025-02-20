import random
# to add:
# after playing Favor the opther player should be able to use a Nope
# What to do if a player has to extract a card but there aren't any
# more cards in the deck?


class Deck:
    def __init__(self, game):
        if game == 'two_players':
            self.deck = (['Exploding Kitten'] * 1
                         + ['Attack'] * 2
                         + ['Defuse'] * 3
                         + ['Cat Cards'] * 12
                         + ['Favor'] * 3
                         + ['See the Future'] * 3
                         + ['Shuffle'] * 2
                         + ['Skip'] * 3)

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

    def add_card(self, card, pos):
        aux = self.deck[:pos]
        aux.append(card)
        aux.extend(self.deck[pos:])
        self.deck = aux


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def show_cards(self):
        print(f'Your cards are \n{self.cards}\n')


class Table:
    # Table contains the discarded cards and the ones used to attack
    def __init__(self):
        self.cards = []   # this is unuseful
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

        # extracting bombs
        bombs = []
        while 'Exploding Kitten' in self.deck.deck:
            bombs.append(self.deck.deck.pop(
                self.deck.deck.index('Exploding Kitten'))
                         )

        # extracting defusers
        defusers = []
        while 'Defuse' in self.deck.deck:
            defusers.append(self.deck.deck.pop(self.deck.deck.index('Defuse')))

        # giving one defuse to each player
        for player in self.players:
            card = defusers.pop()
            player.cards.append(card)

        # put the defuser back in the deck
        while defusers:
            self.deck.deck.append(defusers.pop())

        # shuffle the deck
        self.deck.shuffle()

        for player in self.players:
            for i in range(7):
                card = self.deck.deck.pop()
                player.cards.append(card)

        # adding the bomb to the deck and shuffling again
        while bombs:
            self.deck.deck.append(bombs.pop())
        self.deck.shuffle()

        # it's used to assign the turn to the correct player
        self.player_turn = 0

    def turn(self):
        if len(self.players) == 1:
            print('You won!! Congrats !')
            print('-'*100)
            print('Game developed by bartdzz')
            print('-'*100)
        # choosing the right player for the turn
        player = self.players[self.player_turn]
        players_number = [
                ('You', self.players[i]) if i == self.player_turn
                else (i+1, self.players[i])
                for i in range(len(self.players))]
        print('-'*100)
        print(f"It's {player.name}'s turn")
        self.player_turn = (self.player_turn + 1) % len(self.players)

        # checking if the previous player has used an attack card
        if self.table.attack_cards:
            print(f'Previous attack cards are {self.table.attack_cards}')
            attack_card = self.table.attack_cards.pop(-1)

            if attack_card == 'Attack':
                print(f'Do you want to use one of your cards? [y/n]\n\n'
                      f'Your cards are \n{player.cards}')
                answer = input()

                # checking that we have a valid input
                while answer not in ['y', 'n']:
                    print('You should enter a valid input')
                    print(f'Do you want to use one of your cards? [y/n]'
                          f'\n\nYour cards are \n{player.cards}')
                    answer = input()
                
                # Yes as answer. Use a card: update the player's cards and the
                # table's cards
                if answer == 'y':
                    print(f'Which card do you want to use? [Reply with a number]'
                          f'\n\nYour cards are \n'
                          f'{[((i+1, player.cards[i]) for i in range(len(player.cards)))]}')
                    y = int(input())
                    used_card = player.cards.pop(y-1)
                    used_cards = [used_card]    # this list contains the cards
                                                # played by the current player 
                    self.table.attack_cards.append(used_card)
                    print(f'Now your cards are \n{player.cards}')

                    print('Do you want to use another card? [y/n]')
                    answer = input()
                    while answer != 'n':
                        print(f'Which card do you want to use? (Please in this case reply y just if you want to use Nope or Attack) [Reply with a number]\n\nYour cards are \n{[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                        y = int(input())
                        used_card = player.cards.pop(y-1)
                        self.table.attack_cards.append(used_card)
                        print(f'Now your cards are \n{player.cards}')
                        print('Do you want to use another card? [y/n]')
                        answer = input()
                    
                    if used_card == 'Attack':
                        return    # This player's turn is over
                    else:    # the player uses Nope
                        number_of_nope = sum([1 for x in used_cards if x == 'Nope'])
                        print(f'There have been used {number_of_nope} Nopes')
                        if (number_of_nope < len(self.table.attack_cards) and
                            'Attack' in self.table.attack_cards):
                            self.table.attack_card = self.table.attack_cards[:-number_of_nope]
                            print(f'Attack cards are still {self.table.attack_cards}')
                            n_attack = 1 + sum([
                                                1 for card
                                                in self.table.attack_cards
                                                if card == 'Attack'
                                                ])
                            for _ in range(2*n_attack):
                                if self.deck.deck: # extracting a card from the deck and checking it
                                    card = self.deck.deck.pop(0)
                                    player.cards.append(card)
                                else:
                                    print('No more cards') # WHAT TO DO IF THERE AREN'T ANY MORE CARDS?'
                            self.table.cards.extend(self.table.attack_cards)   # add the attack cards to the table cards
                            self.table.attack_cards = []    # empty the list of attack cards
                        # else : number_of_nope == number of attack_cards

                else:
                    # Player doesn't use any of his cards
                    # take twice as many cards as the number of the attack cards
                    # I have to sum 1 bcs I've popped one 'Attack' card
                    n_attack = 1 + sum([1 for card in self.table.attack_cards if card == 'Attack'])
                    for _ in range(2*n_attack):
                        if self.deck.deck: # extracting a card from the deck and checking it
                            card = self.deck.deck.pop(0)
                            player.cards.append(card)
                        else:
                            print('No more cards') # WHAT TO DO IF THERE AREN'T ANY MORE CARDS?'
                    self.table.cards.extend(self.table.attack_cards)   # add the attack cards to the table cards
                    self.table.attack_cards = []    # empty the list of attack cards

            else:    # here the attack card is 'Nope'
                print(f'Do you want to use one of your cards? [y/n]\nYour cards are {player.cards}')       # I could add the fact that you could just use another 'Nope'
                answer = input()
                while answer not in ['y', 'n']:
                    print('You should enter a valid input')
                    print(f'Do you want to use one of your cards? [y/n]\nYour cards are {player.cards}')
                    answer = input()

                if answer == 'y':
                    print(f'Which card do you want to use? [Reply with a number]\nYour cards are {[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                    y = int(input())
                    used_card = player.cards.pop(y-1)
                    self.table.attack_cards.append(used_card)
                    print(f'Now your cards are {player.cards}')
                    return  # This player's turn is over

                else:
                    self.table.cards.extend(self.table.attack_cards)   # add the attack cards to the table cards
                    self.table.attack_cards = []    # empty the list of attack cards



        # if the previous player hasn't used any attack cards then the turn begins by asking if you want to use a card
        choiche = 'y'
        while choiche == 'y':
            print(f'Your cards are\n{player.cards}\n\nDo you want to use a card? The deck still has {len(self.deck.deck)} cards. [y/n]')
            choiche = input()
            while choiche not in ['y', 'n']:
                print('You should enter a valid input')
                print(f'Your cards are {player.cards}\n\nDo you want to use a card? The deck still has {len(self.deck.deck)} cards [y/n]')
                choiche = input()

            
            if choiche == 'y':    # player chooses to use a card
                print(f'Which card do you want to use? [Reply with a number]\n\nYour cards are {[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                y = int(input())
                used_card = player.cards.pop(y-1)
                if used_card not in ['Attack', 'Favor', 'Cat Cards', 'See the Future', 'Shuffle', 'Skip']:
                    print("You can't use this card")
                    print(f'Which card do you want to use? [Reply with a number]\n\nYour cards are {[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                    y = int(input())

                if used_card == 'Attack':
                    self.table.attack_cards.append(used_card)
                    print(f'Now your cards are\n{player.cards}')
                    answer = 'y'
                    while 'Attack' in player.cards and answer == 'y': 
                        print('Do you want to use another Attack? [y/n]')
                        answer = input()
                        if answer == 'y':
                            index = player.cards.index('Attack')
                            self.table.attack_cards.append(player.cards.pop(index))
                    return print(f"{player.name}'s turn is over")

                else:    # and so used_card in ['Favor', 'Cat Cards', 'See the Future', 'Shuffle', 'Skip']
                    print(f"You're using {used_card}")    
                    if used_card == 'Favor':
                        players_number_names = [(el[0], el[1].name) for el in players_number]
                        print(f"Players are \n{players_number_names}. \nWhich player should do you a favor? [Reply with a number]")
                        x = int(input())
                        player_choosen = self.players[x-1]
                        print(f'{player_choosen.name}, which card do you want to give to {player.name}? [Reply with a number] \n{[(i+1, player_choosen.cards[i]) for i in range(len(player_choosen.cards))]}')
                        x = int(input())
                        choosen_card = player_choosen.cards.pop(x-1)
                        player.cards.append(choosen_card)
                        print(f'Now {player.name}, these are your cards \n{player.cards} and you carry on your turn.')
                    
                    if used_card == 'Cat Cards':
                       cat_cards = [(i+1,player.cards[i]) for i in range(len(player.cards)) if player.cards[i] == 'Cat Cards']
                       if len(cat_cards) == 0:
                           print('To use this card you should have at least 2 cat cards in your hand!')
                           player.cards.append(used_card)
                           # ask to use another card?

                       elif len(cat_cards) == 1:
                            print(f'Which other card do you want to use? [Reply with a number]\n\nYour cards are {[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                            y = int(input()) 
                            player.cards.pop(y-1)
                            # choosing the player to which ask the card
                            players_number_names = [(el[0], el[1].name) for el in players_number]
                            print(f"Players are \n{players_number_names}. \nWhich player should give you a card? [Reply with a number]")
                            x = int(input())
                            player_choosen = self.players[x-1]
                            if len(player_choosen.cards) == 0:
                                print('This player has no cards!')
                            else:
                                print(f'{player_choosen.name} has {len(player_choosen.cards)} cards. Which one do you want? [Reply with a number in 1-{len(player_choosen.cards)}]')
                                x = int(input())
                                choosen_card = player_choosen.cards.pop(x-1)
                                print(f"You've picked {choosen_card}")
                                player.cards.append(choosen_card)
                                # print(f'Now {player.name}, these are your cards \n{player.cards}\n and you carry on your turn.')
                                # the previous command is unuseful since the player sees again his card when the while loop begins again
                       else:
                            print(f'Which card do you want to use? [Reply with two comma separated numbers]\n\nYour cards are {[(i+1, player.cards[i]) for i in range(len(player.cards))]}')
                            y = input().split(',')
                            for i in range(2):
                                player.cards.pop(int(y[i])-1)
                            # choosing the player to which ask the card
                            players_number_names = [(el[0], el[1].name) for el in players_number]
                            print(f"Players are \n{players_number_names}. \nWhich player should give you a card? [Reply with a number]")
                            x = int(input())
                            player_choosen = self.players[x-1]
                            if len(player_choosen.cards) == 0:
                                print('This player has no cards!')
                            else:
                                # FINISH THIS
                                all_cards = ['Exploding Kitten', 'Attack', 'Defuse', 'Cat Cards', 'Favor', 'Nope', 'See the Future', 'Shuffle', 'Skip']
                                all_cards = [(i+1, all_cards[i]) for i in range(len(all_cards))]
                                print(f'All possible cards are:{all_cards}\nWhich card do you want? [Reply with a number]')
                                x = int(input())
                                choosen_card = all_cards.pop(x-1)
                                if choosen_card in player_choosen.cards:
                                    player_choosen.cards.pop(player_choosen.cards.index(choosen_card))
                                    player.cards.append(choosen_card)
                                    print(f'Now {player.name}, these are your cards \n{player.cards}\n and you carry on your turn.')
                                else:
                                    print(f"{player_choosen.name} doesn't have this card!")

                    if used_card == 'See the Future':
                        next_cards = [self.deck.deck[i] for i in range(3)]
                        print(f'The next tree cards in the deck are {next_cards}')

                    if used_card == 'Shuffle':
                        self.deck.shuffle()
                        print("Now the deck has been shuffled")

                    if used_card == 'Skip':
                        print("You've skipped your turn!")
                        return 



                # should add the possibility to use multiple cards
                # must extract a card
        if self.deck.deck: # extracting a card from the deck and checking it
            card = self.deck.deck.pop(0)
            if card == 'Exploding Kitten':
                print('\n\tYOU EXPLODED!\n')
                if 'Defuse' in player.cards:
                    print('You must use your Defuse!')
                    index = player.cards.index('Defuse')
                    player.cards.pop(index)
                    print(f'Now your cards are \n{player.cards}\n')
                    print(f'You have to put the Exploding kitten back in the deck of cards. The deck has {len(self.deck.deck)} cards. \nIn which position do you want to put the bomb? [Reply with a number]')
                    test = True
                    while test:
                        try:
                            x = int(input())
                            test = False
                        except:
                            print('Reply with a number')
                            test = True
                            x = int(input())
                    while x not in range(1, len(self.deck.deck)+2):
                        print('Not a position in the deck!')
                        print('In which position do you want to put the bomb? [Reply with a number]')
                        x = int(input())
                    self.deck.add_card('Exploding Kitten', x-1)
                else:
                    print("You don't have any more Defusers! You lost!")
                    self.players.pop(self.players.index(player))
                    return 
            else:
                print(f'The extracted card is {card}')
                player.cards.append(card)
        else:
            print('No more cards')

        # Asking to show cards
        print('Do you want to see your cards? [y/n]')
        x = input()
        while x not in ['y', 'n']:
            print('Your answer must be in the form y or n')
            x = input()

        if x == 'y':
            player.show_cards()
        else:
            print('All right!')


    def play(self):
        while len(self.players) > 1:
            self.turn()
        return 


