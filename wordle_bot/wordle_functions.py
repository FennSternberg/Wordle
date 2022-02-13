import pandas as pd
import sys, os


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def update_dictionary(colours, guess, data):
    i = 0
    for colour in colours:
        if colour == 'y':
            data = data[data['word'].str.contains(guess[i])]  # keep only words that contain the yellow letter
            data = data[~data['word'].str[i:].str.startswith(
                guess[i])]  # remove all words that contain yellow letter in same position as guess
        elif colour == 'g':
            data = data[data['word'].str[i:].str.startswith(
                guess[i])]  # keep only words that have green letter in same position as guess
        elif colour == 'b':
            data = data[~data['word'].str.contains(guess[i])]  # remove all words that contain black letter

        i += 1
    return data


def get_colours(guess, truth):
    colours = [''] * 5
    for i in range(5):
        if guess[i] == truth[i]:
            colours[i] = 'g'
        elif guess[i] in truth:
            colours[i] = 'y'
        else:
            colours[i] = 'b'
    return colours


def make_guess(guess, truth, data, score):
    score += 1
    print('guess: ' + str(guess))
    if score > 1000:
        print('Exceeded 1000 guesses')
        return score
    if guess == truth:
        print('WINNER WINNER CHICKEN DINNER')
        print('Number of guesses: ' + str(score))
        return score
    else:
        colours = get_colours(guess, truth)
        print('colours: ' + str(colours))
        data = update_dictionary(colours, guess, data)
        data.index = range(0, len(data))
        # always guess first word since this will be the most common
        guess = data.loc[0]['word']
        score = make_guess(guess, truth, data, score)
        return score


def loop_through_games(first_guess, data, no_of_games):
    # Will play x number of wordle games varying the 'true word' starting with first entry in the dictionary
    blockPrint()
    scores = [''] * no_of_games
    for i in range(no_of_games):

        scores[i] = make_guess(first_guess, data['word'][i], data, 0)
        if i % 100 == 0:
            enablePrint()
            print(i)
            print('Current Max Score: ' + str(max(scores[:i + 1])))
            print('Current Mean Score: ' + str(sum(scores[:i + 1]) / (i + 1)))
            blockPrint()
    enablePrint()
    return scores


def read_database():
    db = pd.read_csv('possible_dictionary.csv')
    return db
