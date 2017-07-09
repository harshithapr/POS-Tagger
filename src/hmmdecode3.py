import pickle
import sys
from collections import OrderedDict
import time
from decimal import *
import codecs

start_time = time.time()

def read_modeldata(filename):
    """
    Returns emission and transition probability
    :param(string): filename
    :return: tuple of dictionaries
    """
    fp = open(filename, 'rb')
    pickledata = pickle.load(fp)

    vocab = pickledata[0]
    tag_set = pickledata[1]
    emission_probability = pickledata[2]
    transition_probability = pickledata[3]

    return (vocab, tag_set, emission_probability, transition_probability)

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

def write_output(filename,tag_sequence_list):
    fp=open(filename,'w')
    for tag_sequence in tag_sequence_list:
        sentence=''
        for word in tag_sequence.keys():
            sentence=sentence+word+'/'+tag_sequence[word]+' '
        sentence.rstrip()
        fp.write(sentence)


def pos_tagger(sentences, tag_set, emission_probability, transition_probability,vocab):
    tag_sequence_list=list()
    for sentence in sentences:
        word_list = sentence.strip().split()
        tag_sequence=viterbi_decoder(vocab,tag_set, emission_probability, transition_probability, word_list)
        tag_sequence_list.append(tag_sequence)
    return tag_sequence_list

def viterbi_decoder(vocab_set,tag_set, ep, tp, obsv):
    # Initialization at time t=1
    backp = dict()
    #tag_set.discard('START')
    prev_prob = {'START': Decimal(0.0)}

    #Recursion step for the remaining points
    for t, term in enumerate(obsv):
        prob = {}
        backp[t] = {}
        for q in tag_set:
            if term in vocab_set and ep[q].get(term) is None:
                continue
            #em_p = Decimal.log10(Decimal(0.0000075))
            em_p=Decimal(0.0)
            if term in vocab_set:
                em_p = ep[q][term]
            prob[q], backp[t][q] = max((prev_prob[pq] + tp[pq][q] + em_p, pq) for pq in prev_prob)
        prev_prob = prob
    #Termination step

    _, mostp_end = max((prev_prob[q], q) for q in prev_prob) #Most probable state at end

    #Return the backtrace path by following the backpointers from the most probable state
    pos_tag=mostp_end
    mostp_seq = [pos_tag]
    T = len(obsv)
    for t in reversed(range(1, T)):
        pos_tag = backp[t][pos_tag]
        mostp_seq.append(pos_tag)
    return mostp_seq[::-1]


def write_output(filename,tag_sequence_list,lines):
    fp=open(filename,'w',encoding='utf-8')
    for index,line in enumerate(lines):
        word_list = line.strip().split()
        sentence = ''
        for i in range(0,len(word_list)):
            sentence = sentence + word_list[i] + '/' + tag_sequence_list[index][i] + ' '
        sentence = sentence.rstrip() + '\n'
        fp.write(sentence)

def main():
    print('Decoding')
    #sentences = read_file('catalan_corpus_dev_raw.txt')
    sentences=read_file(sys.argv[1])
    (vocab,tag_set, emission_probability, transition_probability) = read_modeldata('hmmmodel.txt')
    tag_sequence_list = pos_tagger(sentences, tag_set, emission_probability, transition_probability, vocab)
    write_output('hmmoutput.txt', tag_sequence_list,sentences)

if __name__=='__main__':
    main()
    print("\n\n--- %s seconds for entire program ---" % (time.time() - start_time))