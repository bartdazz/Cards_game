import random
class Deck:
    def __init__(self, game):
        if game == 'two_players':
            self.deck = ['Exploding Kitten'] * 1 + ['Attack'] * 2 +['Defuse'] * 3 + ['Cat Cards'] * 12 + ['Favor'] * 3 + ['Nope'] * 3 + ['See the Future'] * 3 + ['Shuffle'] * 2 + ['Skip'] * 3

            for i in range(len(self.deck) - 1):
                r = random.randint(i, len(self.deck) - 1)
                self.deck[i], self.deck[r] = self.deck[r], self.deck[i]
        else:
            print("This game mode hasen't been developed yet")

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

    
    def show_cards(self):
        print(f'Your cards are {self.cards}')

class Match:
    def __init__(self, players, deck):
        '''
        This class represents a match.

        Input:
            players must be a list of players 

        Output:
            Each player will have a hand of cards
            '''
        self.players = players
        self.deck = deck
        for player in self.players:
            for i in range(6):
                player.cards.append(self.deck.deck.pop())
   
        self.player_turn = 0


    def turn(self):

        #choosing the right player for the turn
        player = self.players[self.player_turn]
        print(f"It's {player.name}'s turn")
        self.player_turn = (self.player_turn + 1) % len(self.players)
        
        #extracting a card from the deck and eventually checking it
        if self.deck.deck:
            card = self.deck.deck.pop(0)
            player.cards.append(card)
        else:
            print('No more cards')

        print(f'The extracted card is {card}')
        print('Do you want to see your cards? [y/n]')
        x = input()
        while x not in ['y', 'n']:
            print('Your answer must be in the form y or n')
            x = input()

        if x == 'y':
            player.show_cards()
        else:
            print('All right!')

        print('Do you want to discard a cart or do you want to use one? [d/u]')
        x = input()
        while x not in ['d', 'u']:
            print('Your answer must be in the form y or n')
            x = input()
        
        cards_number = [(i+1, player.cards[i]) for i in range(len(player.cards))]
        if x == 'd':
            print(f'Which card do you want to discard? [Reply with a number]\nYour cards are {cards_number}')
            y = int(input())
            player.cards.pop(y-1)
            print(f'Now your cards are {player.cards}')
        else:
            print(f'Which card do you want to use? [Reply with a number]\nYour cards are {cards_number}')
            y = int(input())
            player.cards.pop(y-1)
            print(f'Now your cards are {player.cards}')



