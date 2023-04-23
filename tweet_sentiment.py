import json
import sys
from collections import defaultdict


def lines(fp):
    print(len(fp.readlines()))


def get_word_and_score(line):
    a, b = line.split("\t")
    c = b.split("\n")
    return a, c[0]


def main():
    with open('sample.json', 'w') as openfile:
        afinn = defaultdict(int)
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
        for line in sent_file.readlines():
            word, score = get_word_and_score(line)
            afinn[word] = int(score)
        for line in tweet_file.readlines():
            data = json.loads(line)
            text = data['text'].lower()
            score = 0
            for word in text.split(" "):
                score += afinn[word]
            openfile.write(str(score) + "\n")


if __name__ == '__main__':
    main()
