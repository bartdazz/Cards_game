from game import *
d = Deck('two_players')
#d.show_deck()
Ali = Player('Alice')
Bart = Player('Bart')
m = Match([Ali, Bart], d)
#print(d.deck.pop(0))
#d.show_deck()
Ali.show_cards()
m.turn()
#d.show_deck()
#m.turn()
