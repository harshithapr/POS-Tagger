import sys

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


def extract_tags(lines):
    tags=[]
    for line in lines:
        terms = line.strip().split()
        for term in terms:
            tags.append(term.split('/')[-1])
    return tags

def accuracy_score(x, y):
    correct = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            correct += 1
    return (correct / len(x)) * 100

def main():
    print('Evaluate')

    #with open('catalan_corpus_dev_tagged.txt') as fid:
    actual_lines = read_file('catalan_corpus_dev_tagged.txt')


    #with open('hmmoutput.txt') as fp:
    pred_lines=read_file('hmmoutput.txt')



    pred_tags = extract_tags(pred_lines)
    actual_tags = extract_tags(actual_lines)

    print('Accuracy score:',accuracy_score(pred_tags,actual_tags))


if __name__=='__main__':
    main()