import copy
import random
import pygame

pygame.init()

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4  # number of decks used to play
game_deck = copy.deepcopy(decks * one_deck)

# setup for the blackjack with pygame
WIDTH = 600
HEIGHT = 900
pygame.display.set_caption('Blackjack')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False

# win, lost, push/draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = [
    '',
    'Player Busted',
    'Player Wins!',
    'Dealer Wins',
    'Push',
    'Blackjack!',
    'Dealer Blackjack'
]


# drawing game
def draw_game(act, record, result):
    button_list = {}

    # on start up (not active), only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('Deal Hand', True, 'black')
        screen.blit(deal_text, (190, 50))
        button_list['deal'] = deal

    # once game started, show hit and stand buttons and win/loss records
    else:
        # hit
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('Hit Me', True, 'black')
        screen.blit(hit_text, (80, 730))
        button_list['hit'] = hit

        # stand
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('Stand', True, 'black')
        screen.blit(stand_text, (385, 730))
        button_list['stand'] = stand

        # score
        score_text = smaller_font.render(
            f"Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}",
            True,
            'white'
        )
        screen.blit(score_text, (15, 840))

    # if there's an outcome for the hand that was played, display a restart button and tell user what occurred
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('New Hand', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list['new_hand'] = deal

    # show a warning when the remaining shoe is low
    if len(game_deck) < 20:
        warning = smaller_font.render('Deck Low!', True, 'yellow')
        screen.blit(warning, (400, 10))

        # only allow manual refill when a hand is not currently being played
        if not hand_active:
            replenish_btn = pygame.draw.rect(screen, 'white', [180, 800, 240, 60], 0, 5)
            pygame.draw.rect(screen, 'red', [180, 800, 240, 60], 3, 5)
            screen.blit(smaller_font.render('REFILL DECK', True, 'black'), (200, 810))
            button_list['refill'] = replenish_btn

    return button_list


# dealing cards by selecting randomly from deck and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + (70 * i), 465 + (5 * i)))
        screen.blit(font.render(player[i], True, 'black'), (75 + (70 * i), 635 + (5 * i)))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + (70 * i), 335 + (5 * i)))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render('???', True, 'black'), (75 + (70 * i), 335 + (5 * i)))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# calculate hand score, check how many aces we have
# pass in player or dealer hand and get the best score
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')

    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - add the number to the total value
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10

        # for aces start by adding 11, check if we need to reduce the value afterward
        elif hand[i] == 'A':
            hand_score += 11

    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10

    return hand_score


# check whether a two-card hand is a natural blackjack
def is_blackjack(hand):
    return len(hand) == 2 and calculate_score(hand) == 21


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score: {player}', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score: {dealer}', True, 'white'), (350, 100))


# add the completed hand result to the win/loss/draw record
def update_record(result, totals):
    if result in [1, 3, 6]:
        totals[1] += 1
    elif result in [2, 5]:
        totals[0] += 1
    elif result == 4:
        totals[2] += 1

    return totals


# set the outcome of a completed hand and update records once
def finish_hand(result):
    global outcome, hand_active, reveal_dealer, records, add_score

    outcome = result
    hand_active = False
    reveal_dealer = True

    if add_score:
        records = update_record(result, records)
        add_score = False


# compare player and dealer once dealer has completed their turn
def check_endgame(deal_score, play_score):
    if play_score > 21:
        return 1
    elif deal_score > 21:
        return 2
    elif play_score > deal_score:
        return 2
    elif play_score < deal_score:
        return 3
    else:
        return 4


# replenish deck when it is low
def replenish_deck():
    global game_deck
    game_deck = copy.deepcopy(decks * one_deck)


# prepare a new hand without recreating the entire shoe every round
def start_new_hand():
    global active, initial_deal, my_hand, dealer_hand
    global outcome, hand_active, reveal_dealer, add_score
    global dealer_score, player_score

    # automatically create a fresh shoe before a new hand if fewer than 20 cards remain
    if len(game_deck) < 20:
        replenish_deck()

    active = True
    initial_deal = True
    my_hand = []
    dealer_hand = []
    outcome = 0
    hand_active = True
    reveal_dealer = False
    add_score = True
    dealer_score = 0
    player_score = 0


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with background color
    timer.tick(fps)
    screen.fill('black')

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)

        player_blackjack = is_blackjack(my_hand)
        dealer_blackjack = is_blackjack(dealer_hand)

        # correctly handle natural blackjack for either or both sides
        if player_blackjack and dealer_blackjack:
            finish_hand(4)
        elif player_blackjack:
            finish_hand(5)
        elif dealer_blackjack:
            finish_hand(6)

        initial_deal = False

    # once game is activated and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)

        # dealer plays automatically after the player stands or reaches 21
        if reveal_dealer and not hand_active and outcome == 0:
            if player_score > 21:
                finish_hand(1)

            elif dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                dealer_score = calculate_score(dealer_hand)

            else:
                finish_hand(check_endgame(dealer_score, player_score))

        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    # event handling, if quit pressed then quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            # initial deal hand button
            if 'deal' in buttons and buttons['deal'].collidepoint(event.pos):
                start_new_hand()

            # hit button - only available while the current player hand is active
            elif (
                'hit' in buttons
                and buttons['hit'].collidepoint(event.pos)
                and outcome == 0
                and hand_active
                and player_score < 21
            ):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                player_score = calculate_score(my_hand)

                # immediately end the player's turn on bust or 21
                if player_score > 21:
                    finish_hand(1)
                elif player_score == 21:
                    hand_active = False
                    reveal_dealer = True

            # stand button
            elif (
                'stand' in buttons
                and buttons['stand'].collidepoint(event.pos)
                and outcome == 0
                and hand_active
            ):
                reveal_dealer = True
                hand_active = False

            # new hand button after a completed result
            elif 'new_hand' in buttons and buttons['new_hand'].collidepoint(event.pos):
                start_new_hand()

            # manual shoe refill button, only shown when no hand is active
            elif 'refill' in buttons and buttons['refill'].collidepoint(event.pos):
                replenish_deck()

    pygame.display.flip()

pygame.quit()
