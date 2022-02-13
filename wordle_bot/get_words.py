"""
unigram_freq.csv is database of the most common english words,
this extracts all those with length 5
"""
import pandas as pd


def read_text(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


df = pd.read_csv('data/archive/unigram_freq.csv')
five = df[df['word'].str.len() == 5]
five.index = range(0, len(five))
print(five)
five.to_csv('five_word_dictionary.csv')  # database of all five-letter words and how common they are
answers = read_text('data/wordle-answers-alphabetical.txt')  # list of all possible wordle answers
answers = pd.DataFrame(answers)
answers = answers.rename(columns={0: 'word'})
ordered_possible_answers = pd.merge(five, answers, how='inner', on=[
    'word'])  # keep only five letter word database entries that are also possible wordle answers
new_row = {'word': 'wooer', 'count': 16161}
ordered_possible_answers = ordered_possible_answers.append(new_row,
                                                           ignore_index=True)  # add word 'wooer' that didnt exist in original database
ordered_possible_answers.to_csv(
    'possible_dictionary.csv')  # database of all possible wordle answers and how common they are
