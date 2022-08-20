# hangman_game_CR.py
# 2022-07-01 | CR

import os
import random
from decorator_execution_time import execution_time
from decorator_press_a_key import press_a_key

WORDS_FILE_SPEC = './files/hangman_data.txt'

HANGMAN_IMAGES = ['''

   +---+
   |   |
       |
       |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
       |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
   |   |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|   |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
  /    |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
  / \  |
       |
 =========''']


# words_to_select : list(str) = []
words_to_select = []
points_awarded = 0


def normalize(s):
    # https://micro.recursospython.com/recursos/como-quitar-tildes-de-una-cadena.html
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


def get_random_word():
    global words_to_select
    random_word : int = random.randint(0, len(words_to_select)-1)
    return words_to_select[random_word]


def get_word_to_display(word_to_be_discovered, user_letters_input):
    word_to_display = []
    for letter in word_to_be_discovered:
        word_to_display.append(letter if letter in user_letters_input else '_')
    return ' '.join(word_to_display)


def show_hangman_image(user_failed_attemps):
    print(HANGMAN_IMAGES[user_failed_attemps])


def user_wins(word_to_be_discovered, user_letters_input):
    return not '_' in get_word_to_display(word_to_be_discovered, user_letters_input)


@press_a_key(msg='Presionar ENTER para jugar de nuevo, o "T" para terminar: ')
# @press_a_key() # Si no se va a pasar el parametro, se debe obligatoriamente poner los parentesis.
@execution_time
def play_game():
    global points_awarded
    word_to_be_discovered_original = get_random_word()
    word_to_be_discovered = normalize(word_to_be_discovered_original.lower())
    user_letters_input = []
    user_failed_attemps = 0
    user_win = False
    attemp = 0
    letters_already_entered = []
    letter_already_entered = None

    while True:
        word_to_display = get_word_to_display(word_to_be_discovered, user_letters_input)
        attemp += 1
        screen_cleaning()
        show_hangman_image(user_failed_attemps)
        print()
        if letter_already_entered != None:
            if letter_already_entered == '':
                print('Por favor introduce alguna letra')
            else:
                print('Es letra "' + user_input + '" ya la jugaste, intenta con una nueva...')
            print()
            letter_already_entered = None
        print('Attemp: ' + str(attemp))
        print()
        print(word_to_display)
        print()
        user_input = input('Introduce una letra: ')
        user_input = normalize(user_input).lower()    
        if user_input in letters_already_entered or user_input == '':
            letter_already_entered = user_input
        elif user_input in word_to_be_discovered:
            user_letters_input.append(user_input)
            if user_wins(word_to_be_discovered, user_letters_input):
                user_win = True
                break
        else:
            user_failed_attemps += 1
            if user_failed_attemps >= len(HANGMAN_IMAGES)-1:
                break
        letters_already_entered.append(user_input)

    if user_win:
        points_awarded += 1
        screen_cleaning()
        show_hangman_image(user_failed_attemps)
        print('Attemps: ' + str(attemp))
        print()
        print('Ganaste 🥳')
        print('La palabra fue: ' + word_to_be_discovered_original)
    else:
        screen_cleaning()
        show_hangman_image(len(HANGMAN_IMAGES)-1)
        print()
        print('Perdiste 😔')
        print('La palabra era: ' + word_to_be_discovered_original)

    print()
    print('Puntos acumulados: ' + str(points_awarded))
      

def run():
    global words_to_select
    words_reading_response = read_words_file()
    if words_reading_response['error']:
        print('ERROR: ' . words_reading_response['error_msg'])
    else:
        words_to_select = words_reading_response['words_list']
        while True:
            key_pressed, response_func = play_game()
            if key_pressed.upper() == 'T':
                break


def read_words_file():
    response = {
        'error': False,
        'error_msg': '',
        'words_list': []
    }
    try:
        with open(WORDS_FILE_SPEC, 'r', encoding='utf-8') as f:
            # Ref: https://stackoverflow.com/questions/12330522/how-to-read-a-file-without-newlines
            response['words_list'] = [row.rstrip('\n') for row in f]
    except BaseException as ve:
        response['error'] = True
        response['error_msg'] = ve
    return response


def screen_cleaning():
    # Clearing the Screen
    # posix is os name for linux or mac
    if os.name == 'posix':
        os.system('clear')
    else:
        # else screen will be cleared for windows
        os.system('cls')


if __name__ == '__main__':
    run()

