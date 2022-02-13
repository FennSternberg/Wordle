import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Results:
    def __init__(self, scores_file, dictionary_file):
        self.scores = np.asarray(read_results(scores_file))
        self.dictionary = pd.read_csv(dictionary_file)['word'].tolist()  # will be in exact same order as self.scores
        self.mean = np.mean(self.scores)
        self.median = np.median(self.scores)
        self.max = np.amax(self.scores)
        self.freq_dist = frequency_distribution(self.scores)

    def running_mean(self, window):
        d = pd.Series(self.scores)
        return d.rolling(window).mean()

    def plot_running_mean(self, window):
        y = self.running_mean(window)
        plt.title('Running mean, window = ' + str(window))
        plt.xlabel("'true word' usage rank")
        plt.ylabel('Number of guesses')
        plt.plot(y)
        return

    def plot_freq_dist(self):
        # plots frequency of each score
        unique, counts = np.unique(self.scores, return_counts=True)
        plt.title('Frequency distribution of different scores')
        plt.ylabel('% of total games')
        plt.xlabel('number of guesses')
        plt.bar(unique, 100 * counts / np.sum(counts))


def read_results(filename):
    with open(filename) as file:
        lines = [int(line.rstrip()) for line in file]
    return lines


def frequency_distribution(scores):
    unique, counts = np.unique(scores, return_counts=True)
    return np.asarray((unique, counts)).T


fwd = Results('fwd_results.txt', 'five_word_dictionary.csv')  # results of game with five word dictionary database
