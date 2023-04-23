import sys
import json

def extract_hashtags(tweet):
    """Extracts hashtags from a tweet object"""
    hashtags = []
    entities = tweet.get('entities', {})
    for hashtag in entities.get('hashtags', []):
        text = hashtag.get('text', '').lower()
        if text:
            hashtags.append(text)
    return hashtags

def main():
    # Load tweet file
    tweet_file = open(sys.argv[1], 'r')

    # Count hashtags
    hashtag_counts = {}
    for line in tweet_file:
        tweet = json.loads(line)
        hashtags = extract_hashtags(tweet)
        for hashtag in hashtags:
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1

    # Print top ten hashtags
    top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for hashtag, count in top_hashtags:
        print('{} {}'.format(hashtag, count))

if __name__ == '__main__':
    main()
