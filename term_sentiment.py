import json
import sys
from collections import defaultdict
import re


def lines(fp):
    print(len(fp.readlines()))

def get_sentiments(fs):
    afinn = {}
    for line in fs.readlines():
        word, score = line.split("\t")
        afinn[word] = int(score)
    return afinn

def get_sentiment_from_tweet(text, sentiments):
    score = 0
    for word in text.split():
        if word in sentiments:
            score += sentiments[word]
    return score

def extract_words(text):
    # Remove URLs from text
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www.\S+', '', text)

    # Split text into words
    words = re.findall(r'\w+', text.lower())

    return words


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    lines(sent_file)
    lines(tweet_file)
    sentiments = get_sentiments(sent_file)
    new_words = {}
    word_counts = {}
    for line in tweet_file.readlines():
        tweet = json.loads(line)
        text = tweet["text"].lower()
        sentiment = get_sentiment_from_tweet(text, sentiments)
        for word in extract_words(text):
            if word not in sentiments:
                if word not in new_words:
                    new_words[word] = sentiment
                    word_counts[word] = 1
                else:
                    new_words[word] += sentiment
                    word_counts[word] += 1
    print(len(new_words))
    for word in new_words:
        score = new_words[word] / float(word_counts[word])
        print("{} {}".format(word, score))

if __name__ == '__main__':
    main()
