'''
Required packages: pillow
'''

import random
import requests
import time
from PIL import Image

# start round by asking player if they're ready
# function will keep asking until they say yes
def start_game():
    r1 = input('Are you ready to play? (y/n) ').lower()
    if r1 == 'y' or r1 == 'yes':
        print(' ')
        print('Let\'s goooooo')
    elif r1 == 'n' or r1 == 'no':
        print('')
        print('OK. Hit y when you\'re ready')
        start_game()
    else:
        print('')
        print('What?')
        start_game()

# function creates a random pokemon 'card' by generating random ID number and accessing API
# parameters-
#   player:
#   'y' = you
#   'c' = the computer
# prints stats and displays image of the pokemon
# returns pokemon 'card' (dictionary of stats)
def generate_card(player):
    pokenumber = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokenumber)
    response = requests.get(url)
    pokemon = response.json()
    pokemon_card = {'name':pokemon['name'],
                    'height':pokemon['height'],
                    'weight':pokemon['weight'],
                    'base_experience':pokemon['base_experience'],
                    'hp':pokemon['stats'][0]['base_stat'],
                    'attack':pokemon['stats'][1]['base_stat'],
                    'defence':pokemon['stats'][2]['base_stat'],
                    'image url':pokemon['sprites']['front_default']}
    if player == 'y':
        text = 'Your'
    elif player == 'c':
        text = 'The computer\'s'
    print('{} pokemon is...'.format(text))
    print(pokemon_card['name'].title())
    image = Image.open(requests.get(pokemon_card['image url'], stream=True).raw)
    image.show()
    print('Height: {}'.format(pokemon_card['height']))
    print('Weight: {}'.format(pokemon_card['weight']))
    print('Base experience: {}'.format(pokemon_card['base_experience']))
    print('HP: {}'.format(pokemon_card['hp']))
    print('Attack: {}'.format(pokemon_card['attack']))
    print('Defence: {}'.format(pokemon_card['defence']))
    return pokemon_card


# function decides on a stat to compare, either by asking player or by having computer generate random choice
# returns 'choice', the key title for that stat, which is later used to access the value from the card dictionary
# parameters-
#   player:
#   'y' = you
#   'c' = the computer
def get_choice(player):
    stat_list = ['height', 'weight', 'base experience', 'hp', 'attack', 'defence']
    if player == 'y':
        while True:
            chosen_stat = input('Which stat do you choose? ').lower()
            if chosen_stat in stat_list:
                break
            print('Invalid choice. Please choose height, weight, base experience, HP, attack, or defence')
        print('You chose to compare {}.'.format(chosen_stat))
    elif player == 'c':
        random_stat = random.randint(1, 6)
        if random_stat == 1:
            chosen_stat = 'height'
        if random_stat == 2:
            chosen_stat = 'weight'
        if random_stat == 3:
            chosen_stat = 'base experience'
        if random_stat == 4:
            chosen_stat = 'hp'
        if random_stat == 5:
            chosen_stat = 'attack'
        if random_stat == 6:
            chosen_stat = 'defence'
        print('The computer chose to compare {}.'.format(chosen_stat))
    if chosen_stat != 'base experience':
        choice = chosen_stat
    if chosen_stat == 'base experience':
        choice = 'base_experience'
    print('')
    return choice

# compare chosen stat on the player's and the computer's pokemon cards, reveal winner
# player and computer score 1 point for winning, and 0 points for losing. If it's a draw, both score 0
# returns list containing round result in 0th position, player score in 1st position, and computer's score in 2nd position
# parameters-
#   stat: chosen stat to compare
#   your_card: dictionary of stats on your pokemon
#   comp_card: dictionary of stats on the computer's pokemon
def game_result(stat, your_card, comp_card):
    your_score = your_card['{}'.format(stat)]
    comp_score = comp_card['{}'.format(stat)]
    if your_score > comp_score:
        result = 'WIN'
        your_points = 1
        computer_points = 0
    elif comp_score > your_score:
        result = 'LOSE'
        your_points = 0
        computer_points = 1
    elif your_score == comp_score:
        result = 'DRAW'
        your_points = 0
        computer_points = 0
    print('')
    print('You scored {} and the computer scored {}...'.format(your_score, comp_score))
    print('You {} this round!'.format(result))
    return result, your_points, computer_points

# function plays one round of top trumps
# time delays added to pace game
def play_round(chooser):
    start_game()
    time.sleep(2)
    print('')
    your_card = generate_card('y')
    print('')
    time.sleep(2)
    comparison_stat = get_choice('{}'.format(chooser))
    print('')
    time.sleep(2)
    comp_card = generate_card('c')
    print('')
    time.sleep(2)
    result = game_result(comparison_stat, your_card, comp_card)
    return result

# function plays a game of multiple rounds
# and saves results to a text file??
# parameters-
#   number_rounds: number of rounds in game
def play_game(number_rounds):
    you = input('What\'s your name? ')
    file_name = you + 'vscomputer'
    your_total_wins = 0
    comp_total_wins = 0
    with open('{}.txt'.format(file_name), 'w+') as text_file:
        title = 'Top Trumps: {} vs the computer \n '.format(you)
        text_file.write(title)
    for game in range(1, (number_rounds+1)):
        print('')
        print('Round {}'.format(game))
        print('')
        if (game % 2) != 0:
            chooser = 'y'
        elif (game % 2) == 0:
            chooser = 'c'
        round_result = play_round(chooser)
        your_total_wins += round_result[1]
        comp_total_wins += round_result[2]
        with open('{}.txt'.format(file_name), 'r') as text_file:
            current_text = text_file.read()
        round_summary = 'Round {} result: {}.'.format(game, round_result[0])
        new_text = current_text + '\n' + round_summary + '\n'
        with open('{}.txt'.format(file_name), 'w+') as text_file:
            text_file.write(new_text)
    if your_total_wins > comp_total_wins:
        who_won = 'You'
    elif your_total_wins < comp_total_wins:
        who_won = 'The computer'
    elif your_total_wins == comp_total_wins:
        who_won = 'Nobody'
    game_summary = '\n You won {} round(s) and the computer won {} round(s). {} won the game!'.format(your_total_wins, comp_total_wins, who_won)
    with open('{}.txt'.format(file_name), 'r') as text_file:
        current_text2 = text_file.read()
    final_text = current_text2 + '\n' + game_summary + '\n'
    with open('{}.txt'.format(file_name), 'w+') as text_file:
        text_file.write(final_text)
    print(game_summary)
    print('See {}.txt for game summary'.format(file_name))

play_game(2)
