import sys
import json
import re
from collections import defaultdict

us_states = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}



# Load the AFINN sentiment dictionary
def load_afinn(fs):
    afinn = {}
    for line in fs.readlines():
        word, score = line.split("\t")
        afinn[word] = int(score)
    return afinn

# Compute the sentiment score of a tweet
def compute_sentiment(tweet, afinn):
    sentiment = 0
    if 'text' in tweet:
        # Get the text of the tweet and split it into individual terms
        tweet_text = tweet['text']
        terms = tweet_text.split()

        # Compute the sentiment score for each term in the tweet
        for term in terms:
            # Remove non-alphanumeric characters from the beginning and end of the term
            term = term.strip('\'"?,.!:-\';()[]{}')
            # Convert the term to lowercase
            term = term.lower()
            # Ignore terms that are too short or contain non-alphabetic characters
            if len(term) < 2 or not term.isalpha():
                continue

            # Look up the sentiment score for the term in the AFINN dictionary
            if term in afinn:
                sentiment += afinn[term]

    return sentiment

# Determine the state of a tweet based on its location metadata
def get_tweet_state(tweet):
    state = None
    if 'place' in tweet and tweet['place'] is not None:
        # Use the state abbreviation dictionary to check if the place is in the United States
        country = tweet['place']['country_code']
        if country == 'US':
            # Check if the place contains a state abbreviation
            place_fullname = tweet['place']['full_name']
            for abbr, fullname in us_states.items():
                if fullname in place_fullname:
                    state = abbr
                    break

    elif 'user' in tweet and tweet['user'] is not None:
        # Use the user location metadata to determine the state
        location = tweet['user']['location']
        if location is not None:
            location = location.lower()
            # Check if the location contains a state abbreviation
            for abbr, fullname in us_states.items():
                if abbr.lower() in location or fullname.lower() in location:
                    state = abbr
                    break

    return state


if __name__ == '__main__':

    state_scores = defaultdict(int)
    state_counts = defaultdict(int)
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # Load the sentiment scores into a dictionary
    afinn = load_afinn(sent_file)

    # Iterate over each tweet in the file
    for tweet in tweet_file:
        tweet_dict = json.loads(tweet)

        # Check if the tweet contains the 'text' key
        if 'text' in tweet_dict:
            # Get the sentiment of the tweet and the state it
            state = get_tweet_state(tweet_dict)
            if state:
                sentiment = compute_sentiment(tweet_dict, afinn)
                state_scores[state] += sentiment
                state_counts[state] += 1

    state_averages = {}
    for state in state_scores:
        if state_counts[state] > 0:
            state_averages[state] = state_scores[state] / state_counts[state]

    happiest_state = max(state_averages, key=state_averages.get)

    print(us_states[happiest_state])
