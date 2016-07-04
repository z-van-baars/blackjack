import random


class Player(object):
    def __init__(self, name):
        self.name = name
        self.coins = 0
        self.hands = []
        self.split_made_this_round = False
        self.moves_finished = False


class Deck(object):
    def __init__(self):
        self.shuffled_deck = []
        self.discard = []


class Hand(object):
    def __init__(self, name):
        self.cards = []
        self.total = 0
        self.bet = 0
        self.bust = False
        self.blackjack = False
        self.name = name

    def get_card_total(self):
        total = 0
        for each in self.cards:
            total += each[1]
        self.total = total


def another_game():
    choice_made = False
    while not choice_made:
        choice = input("Play another round? [yes / no] \n")
        if choice == "no":
            choice = False
            choice_made = True
        elif choice == "yes":
            choice = True
            choice_made = True
        else:
            print("{ Invalid choice, try again. }")
    return choice


def printouts():
    print('\n' * 50)
    
    if not user.moves_finished:
        print("Dealer's total %d // Dealer's Hand" % (dealer.hands[0]).cards[0][1])
        print("_____________________________________")
        print((dealer.hands[0]).cards[0][0] + " | FACE DOWN", end=" | ")
    else:
        print("Dealer's total %d // Dealer's Hand" % dealer.hands[0].total)
        print("_____________________________________")
        for card in (dealer.hands[0]).cards:
            print(card[0], end=" | ")
    print("\n \n")
    print("Player's Coins: %d \n" % user.coins)
    hand_number = 0
    for hand in user.hands:
        hand_number += 1
        print("Hand # %d // Bet: %d // Card Total %d // Cards" % ((hand_number), (hand.bet), (hand.total)))
        print("______________________________________________\n  ")
        for card in hand.cards:
            print(card[0], end=" | ")
        print("\n______\n")


def hit(player_hitting, hand):
    new_card = random.choice(active_deck.shuffled_deck)
    active_deck.shuffled_deck.remove(new_card)
    print(player_hitting.name + " draws " + new_card[0])
    input(" > Hit Enter to continue")
    hand.cards.append(new_card)


def stay(player_staying, hand):
    print(player_staying.name + " stays")
    input(" > Hit Enter to continue")


def split(player_splitting, hand):
    hand_number = str(len(player_splitting.hands) + 1)
    new_hand = Hand(hand_number)
    bet_copy = hand.bet
    new_hand.bet = bet_copy
    new_hand.cards.append(hand.cards[1])
    hand.cards.remove(hand.cards[1])
    player_splitting.hands.append(new_hand)
    for each in player_splitting.hands:
        hit(player_splitting, each)
        each.get_card_total()


def dealer_choice(hand):
    printouts()
    dealer_not_staying = True
    while dealer_not_staying and not hand.bust:

        if hand.total < 17:
            hit(dealer, hand)
        elif hand.total == 17:
            soft_seventeen = False
            for each in hand.cards:
                if each[1] == 11:
                    soft_seventeen = True
            if not soft_seventeen:
                stay(dealer, hand)
                dealer_not_staying = False
            else:
                hit(dealer, hand)
                bust_check(dealer, hand)
        elif hand.total > 17:
            stay(dealer, hand)
            dealer_not_staying = False
        hand.get_card_total()
        bust_check(dealer, hand)
        printouts()


def player_choice(hand):
    player_not_staying = True
    while player_not_staying and not hand.bust:
        player_action_chosen = False
        while not player_action_chosen:
            print("Do what? (Hand # %s) Hit / Stay / Double Down / Split" % hand.name)
            player_choice = input("?")
            if player_choice == "hit":
                hit(user, hand)
                player_action_chosen = True
            elif player_choice == "stay":
                stay(user, hand)
                player_not_staying = False
                player_action_chosen = True
            elif player_choice == "double":
                if (user.coins - hand.bet) >= hand.bet:
                    print("Double Down activated!  User bets an additional %d coins and gets one more card!" % hand.bet)
                    input("Hit Enter to continue!")
                    hand.bet *= 2
                    hit(user, hand)
                    player_not_staying = False
                    player_action_chosen = True
                else:
                    print("Not enough coins left to double down!  Pick another action.")
            elif player_choice == "split" and len(hand.cards) == 2:
                if hand.cards[0][1] == hand.cards[1][1]:
                    split(user, hand)
                    player_action_chosen = True
                else:
                    print("Not a valid hand for a split, try again.")
            else:
                print("not a valid choice, try again")
        hand.get_card_total()
        bust_check(user, hand)
        printouts()


def bust_check(player_to_be_checked, hand_to_be_checked):
    if hand_to_be_checked.total > 21:
        hand_to_be_checked.bust = True
        ace_check_hand = []
        ace_demoted_already = False
        for card in hand_to_be_checked.cards:
            if card[1] == 11 and not ace_demoted_already:
                print("moving an Ace to a 1")
                ace_check_hand.append((card[0], 1))
                ace_demoted_already = True
                hand_to_be_checked.bust = False
            else:
                ace_check_hand.append(card)
        hand_to_be_checked.cards = ace_check_hand
        hand_to_be_checked.get_card_total()

    if hand_to_be_checked.bust:
        print(player_to_be_checked.name + " busts!")


def place_bet(hand):
    player_bet_made = False
    while not player_bet_made:
        while True:
            try:
                print("Bet how much. Your coins: %s" % user.coins)
                x = int(input("? "))
                break
            except ValueError:
                print("Invalid bet amount, try again")
                pass

        if x in range(1, (user.coins + 1)):
            hand.bet = x
            print("Player bet %d coins!" % hand.bet)
            player_bet_made = True
        else:
            print("Invalid bet amount, try again")


def new_hand():
    print("New Hand!")
    input(" > Hit Enter to continue!")
    new_hand = Hand("1")
    place_bet(new_hand)
    for user_cards in range(2):
        new_card = random.choice(active_deck.shuffled_deck)
        active_deck.shuffled_deck.remove(new_card)
        new_hand.cards.append(new_card)
    user.hands.append(new_hand)
    for hand in user.hands:
        hand.get_card_total()
        if hand.total == 21:
            hand.blackjack = True
            input("User gets Blackjack! Hit Enter to continue")
    new_hand = Hand("1")
    for dealer_cards in range(2):
        new_card = random.choice(active_deck.shuffled_deck)
        active_deck.shuffled_deck.remove(new_card)
        new_hand.cards.append(new_card)
    dealer.hands.append(new_hand)
    for hand in dealer.hands:
        hand.get_card_total()
        if hand.total == 21:
            hand.blackjack = True
            input('Dealer gets Blackjack! Hit Enter to continue')


def player_wins(hand):
    print("Player wins!")
    print("Player wins %s coins!" % str(hand.bet))
    user.coins += hand.bet


def dealer_wins(hand):
    print("Dealer wins!")
    print("Player loses %s coins!" % str(hand.bet))
    user.coins -= hand.bet


def win_check():
    for hand in user.hands:
        if (dealer.hands[0]).total > hand.total:
            if hand.bust and (dealer.hands[0]).bust:
                print("Push! Both players tie.")
            else:
                if not (dealer.hands[0]).bust and not hand.bust:
                    dealer_wins(hand)
                else:
                    print("Dealer busts!")
                    player_wins(hand)

        elif (dealer.hands[0]).total < hand.total:
            if hand.bust and (dealer.hands[0]).bust:
                print("Push! Both players tie.")
            else:
                if not hand.bust and not (dealer.hands[0]).bust:
                    player_wins(hand)
                else:
                    print("Player busts!")
                    dealer_wins(hand)

        else:
            print("Push! Both players tie.")


def cleanup(player_to_be_cleaned):
    for hand in player_to_be_cleaned.hands:
        for card in hand.cards:
            active_deck.discard.append(card)
    player_to_be_cleaned.hands = []
    player_to_be_cleaned.moves_finished = False

def reset_aces():
    for card in active_deck.discard:
        if card[1] == 1:
            active_deck.shuffled_deck.append((card[0], 11))
        else:
            active_deck.shuffled_deck.append(card)

def choose_deck_amount():
    number_of_decks_chosen = False
    while not number_of_decks_chosen:
   
        while True:
            try:
                print("How many decks would you like to play with? 1 // 2 // 3 // 4 // 5 // 6")
                decks = int(input("? "))
                break
            except ValueError:
                print("Invalid deck number, try again")
                pass

        if decks in range(1, 7):
            print("Playing with %d decks!" % decks)
            number_of_decks_chosen = True
        else:
            print("Invalid deck number, try again")
    return decks


playing = True
decks = choose_deck_amount()

card_tuples = []
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
card_values = [("2 of ", 2), ("3 of ", 3), ("4 of ", 4), ("5 of ", 5), ("6 of ", 6), ("7 of ", 7), ("8 of ", 8), ("9 of ", 9), ("10 of ", 10), ("Jack of ", 10), ("Queen of ", 10), ("King of ", 10), ("Ace of ", 11)]
for deck in range(decks):
    for suit in suits:
        for value in card_values:
            card_tuples.append((value[0] + suit, value[1]))

user_name = "User"
user = Player(user_name)
user.coins = 100
dealer = Player("Dealer")
active_deck = Deck()
active_deck.shuffled_deck = card_tuples

while playing:
    random.shuffle(active_deck.shuffled_deck)
    while len(active_deck.shuffled_deck) > 14:
        new_hand()
        input(" > Hit Enter to continue")

        printouts()

        if not (dealer.hands[0]).blackjack:
            for hand in user.hands:
                if not hand.blackjack:
                    player_choice(hand)
        user.moves_finished = True

        busts = 0
        blackjacks = 0
        for hand in user.hands:
            if hand.bust:
                busts += 1
            if hand.blackjack:
                blackjacks += 1

        if busts != len(user.hands) and blackjacks != len(user.hands):
            dealer_choice(dealer.hands[0])

        win_check()
        cleanup(user)
        cleanup(dealer)

    for card in active_deck.shuffled_deck:
        active_deck.discard.append(card)
        active_deck.shuffled_deck.remove(card)
    for card in active_deck.discard:
        active_deck.shuffled_deck.append(card)
        active_deck.discard.remove(card)

    playing = another_game()