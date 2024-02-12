import random

class Card:
    def __init__ (self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
                {'rank': 'A', 'value': 11},
                {'rank': '2', 'value': 2},
                {'rank': '3', 'value': 3},
                {'rank': '4', 'value': 4},
                {'rank': '5', 'value': 5},
                {'rank': '6', 'value': 6},
                {'rank': '7', 'value': 7},
                {'rank': '8', 'value': 8},
                {'rank': '9', 'value': 9},
                {'rank': '10', 'value': 10},
                {'rank': 'J', 'value': 10},
                {'rank': 'Q', 'value': 10},
                {'rank': 'K', 'value': 10},
                ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, n):
        dealt = []
        for i in range(n):
            if(len(self.cards) > 0):
                dealt.append(self.cards.pop())
        return dealt
    

class Hand():
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value

            if(card.rank['rank'] == 'A'):
                has_ace = True

        if(has_ace) and (self.value > 21):
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def is_blackjack(self):
        return self.get_value == 21
    
    def display(self, show_dealer_card=False):
        print(f'''{"Dealer's" if self.dealer == True else "Your"} hand: ''')
        for index, card in enumerate(self.cards):
            if(index == 0) and (self.dealer) and (not show_dealer_card) and (not self.is_blackjack()):
                print("hidden")
            else:
                print(card)

        if not self.dealer:
            print("Value:", self.get_value())

        print()


class Game():
    def play(self):
        game_number = 0
        game_to_play = 0

        while(game_to_play <= 0):
            try:
                game_to_play = int(input("How many games do you want to play? "))
            except:
                print("Enter number only.")

        while(game_number < game_to_play):
            game_number += 1
            deck = Deck()
            deck.shuffle()

            play_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                play_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))
            print()
            print("*" * 30)
            print(f"Game {game_number} of {game_to_play}")
            print("*" * 30)

            play_hand.display()
            dealer_hand.display()

            if self.check_winner(play_hand, dealer_hand):
                continue

            choice = ""
            while play_hand.get_value() < 21 and choice not in ['s', 'stand']:
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ['h', 's', 'hit', 'stand']:
                    choice = input("Please choose 'Hit' or 'Stand': (H/S)").lower()
                    print()

                if choice in ['hit', 'h']:
                    play_hand.add_card(deck.deal(1))
                    play_hand.display()

            if self.check_winner(play_hand, dealer_hand):
                continue

            player_hand_value = play_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_dealer_card=True)
            if self.check_winner(play_hand, dealer_hand):
                continue

            print("Final resuls")
            print("your hand: ", player_hand_value)
            print("dealer hand: ", dealer_hand_value)

            self.check_winner(play_hand, dealer_hand, True)
        
    def check_winner(self, play_hand, dealer_hand, game_over=False):
        if not game_over:
            if play_hand.get_value() > 21:
                print("You busted. Dealer wins!")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted")
                return True
            elif (play_hand.is_blackjack()) and (dealer_hand.is_blackjack()):
                print("Tie!")
                return True
            elif (play_hand.is_blackjack()):                
                print("You win")
                return True
            elif (dealer_hand.is_blackjack()):
                print("Dealer win")
                return True
        else:
            if play_hand.get_value() > dealer_hand.get_value():
                print("You win")
            elif play_hand.get_value() == dealer_hand.get_value():
                print("Tie")
            else:
                print("You lose")
        
        return False
    
g = Game()
g.play()