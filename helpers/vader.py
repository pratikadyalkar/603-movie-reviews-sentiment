from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


####### Write your primary function here
def sentiment_scores(sentence):
    sent_keys = ["Negative", "Neutral", "Positive"]
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    sent_values = [x for x in sentiment_dict.values()]
    sent_values=sent_values[:3]
    # find the index of the max value

    index_max = np.argmax(sent_values)

    # decide sentiment as positive, negative and neutral
    final = sent_keys[index_max]
    # responses
    response1=f"Overall sentiment is {final} with scores: {sentiment_dict}"
    return response1
