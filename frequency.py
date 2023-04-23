import re
import sys
import json


def extract_words(text):
    # Remove URLs from text
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www.\S+', '', text)

    # Split text into words
    words = re.findall(r'\w+', text.lower())

    return words


def main():
    tweet_file = open(sys.argv[1])

    # Initialize a dictionary to store the term frequency counts
    term_freq = {}

    # Iterate over each tweet in the file
    for tweet in tweet_file:
        tweet_dict = json.loads(tweet)

        # Check if the tweet contains the 'text' key
        if 'text' in tweet_dict:
            # Get the text of the tweet and split it into individual terms
            tweet_text = tweet_dict['text']
            terms = extract_words(tweet_text)

            # Update the term frequency counts for each term in the tweet
            for term in terms:
                # Convert the term to lowercase
                term = term.lower()
                # Ignore terms that are too short or contain non-alphabetic characters
                if len(term) < 2 or not term.isalpha():
                    continue

                # Update the term frequency count
                if term in term_freq:
                    term_freq[term] += 1
                else:
                    term_freq[term] = 1

    # Compute the total number of terms in the file
    total_terms = sum(term_freq.values())

    # Compute the term frequencies and print them to stdout
    for term in term_freq:
        freq = term_freq[term] / float(total_terms)
        print('{} {}'.format(term, freq))


if __name__ == '__main__':
    main()
