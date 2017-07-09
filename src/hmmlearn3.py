#!/usr/bin/python
# hmmlearn.py HMM model data
# Usage:
# hmmlearn.py input_filename1
# This program reads the input file, tokenizes each input line, calculate transition and emission probability
# and write the model parameters into the file

import sys
from collections import Counter, defaultdict
from decimal import *
import pickle
import time

p_start_time=time.time()

def read_file(filename):
    """
    Read the text file with the given filename and return a list of lines
    :param(string) filename:
    :return:list of strings
    """
    try:
        trimmed_lines=list()
        fp = open(filename, 'r',encoding="utf-8")
        lines=fp.readlines()
        for line in lines:
            trimmed_lines.append(line.strip())
        return trimmed_lines
    except IOError:
        print('Error opening or reading the file '+filename)
        sys.exit()


def get_vocab_tags(linestrings):
    """

    :param linestrings(list of strings):
    :return:
    """
    vocab_set = set()
    tag_set = set()

    tag_frequency = Counter()  # Dictionary
    word_tag_frequency = defaultdict(Counter)  # Dictionary of Dictionary

    tag_list=[]

    tag_out_frequency = Counter()  # Dictionary
    tag_tag_frequency = defaultdict(Counter)  # Dictionary of Dictionary

    for linestring in linestrings:
        words = linestring.split(' ')
        tag_line=[]
        for word in words:
            token = word[:-3]
            tag = word[-2:].upper()
            vocab_set.add(token)
            tag_set.add(tag)

            tag_frequency[tag] += 1
            word_tag_frequency[tag][token] += 1

            tag_line.append(tag)
        tag_list.append(tag_line)

    for tag_line in tag_list:
        for index in range(0,len(tag_line)-1):
            cur_tag = tag_line[index]  # Fetch the current tag
            next_tag = tag_line[index + 1] # Fetch the next tag
            if (index == 0):  # Find the transition frequency from the start state
                tag_out_frequency['START'] += 1
                tag_tag_frequency['START'][cur_tag] += 1
            # Transition out frequency of a tag
            tag_out_frequency[cur_tag] += 1
            # Transition frequency from previous tag to current tag
            tag_tag_frequency[cur_tag][next_tag] += 1
    return (vocab_set, tag_set, tag_frequency, word_tag_frequency, tag_out_frequency, tag_tag_frequency)

def find_emission_probability(tag_frequency, word_tag_frequency):
    """
    Returns the dictionary of emission probabilty for each pair of word and tag.
    :param tag_frequency(dictionary): Count of each tag
    :param tag_word_frequency(dictionary): Count(word and tag)
    :return: dictionary of emission probabilty
    """
    emission_probability = dict()

    for tag in tag_frequency.keys():
        if emission_probability.get(tag) is None:
            emission_probability[tag] = dict()
        for word in word_tag_frequency[tag]:
            word_count = Decimal(word_tag_frequency[tag][word])
            tag_count = Decimal(tag_frequency[tag])
            emission_probability[tag][word] = Decimal.log10(word_count / tag_count)
            #emission_probability[tag][word]=word_count / tag_count
    return emission_probability

def find_transition_probability(tag_out_frequency, tag_tag_frequency,tags_set):
    """
    Returns the dictionary of emission probabilty for each pair of word and tag.
    :param tag_out_frequency(dictionary): Transition out frequency of each tag
    :param tag_tag_frequency(dictionary): Transition frequency from tag to tag
    :return: dictionary of emission probabilty
    """
    transition_probability = dict()

    for tag1 in tags_set:
        transition_probability[tag1] = dict()
        for tag2 in tags_set:
            tag_tag_count=Decimal(tag_tag_frequency[tag1][tag2])
            tag_out_count=Decimal(tag_out_frequency[tag1])
            total_tags=len(tags_set);
            transition_probability[tag1][tag2] = Decimal.log10((tag_tag_count+1)/ (tag_out_count+total_tags))
    return transition_probability

def write_model(tag_set, emission_probability, transition_probability,vocab):
    """
    Writes the model into a text file using pickle
    :param emission_probability(dictionary): Emission probability
    :param transition_probability(dictionary): Transition Probability
    :return:
    """
    fp=open('hmmmodel.txt','wb')
    pickle_data=[tag_set,emission_probability,transition_probability,vocab]
    pickle.dump(pickle_data,fp)

def main():
    lines = read_file(sys.argv[1])


    (vocab,tags,tag_frequency, word_tag_frequency,tag_out_frequency, tag_tag_frequency)=get_vocab_tags(lines)

    emission_probability = find_emission_probability(tag_frequency, word_tag_frequency)


    tags.add('START')
    transition_probability = find_transition_probability(tag_out_frequency, tag_tag_frequency, tags)

    tags.remove('START')
    write_model(vocab, tags, emission_probability, transition_probability)

if __name__ == '__main__':
    main()
    print("\n\n--- %s seconds for entire program ---" % (time.time() - p_start_time))