import random
BUST_THRESHOLD = 21
DEALER_HIT_THRESHOLD = 17
deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]



def dealCard(deck):
    return random.choice(deck)


def calculateScore(hand):
    total = sum(hand)
    if total == 21 and len(hand) == 2:
        return 0  # Blackjack
    if 11 in hand and total > BUST_THRESHOLD:  # Make an ace worth 1 if player busts
        hand.remove(11)
        hand.append(1)
        total = sum(hand)
    return total


def compare(player, computer):
    response = ""
    player_total = calculateScore(player)
    dealer_total = calculateScore(computer)
    if player_total == dealer_total and player_total <= BUST_THRESHOLD:
        response = "It is a draw."
    elif player_total == 0:
        response = "Blackjack! You win!"
    elif player_total > BUST_THRESHOLD:
        response = "Bust! You lose."
    elif dealer_total == 0:
        response = "Dealer has blackjack! You lose!"
    elif dealer_total > BUST_THRESHOLD:
        response = "Dealer busts! You win!"
    elif player_total > dealer_total:
        response = "You win!"
    else:
        response = "You lose!"
    return response
