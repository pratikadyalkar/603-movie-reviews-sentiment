from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


####### Write your primary function here
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        final="Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        final="Negative"
    else :
        final="Neutral"
    # responses
    response1=f"Overall sentiment is {final} with scores: {sentiment_dict}"
    return response1
