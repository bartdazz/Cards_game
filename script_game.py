from game import *
d = Deck('two_players')
t = Table()
#d.show_deck()
Ali = Player('Alice')
Bart = Player('Bart')
m = Match([Ali, Bart], d, t)
#m.deck.show_deck()
#print("Showing Alice's cards:")
#Ali.show_cards()
#print('-'*60)
#print("Showing Bart's cards:")
#Bart.show_cards()
#print('-'*60)
m.turn()

#d.show_deck()
m.turn()
m.turn()
##m.turn()
#m.turn()
