import json
from pprint import pprint
import time

test_file = '../json/testexchange_testmarket/05222018_025159/comprehend_results.json'

positive_score_threshold = 0.90
negative_score_threshold = 0.90


if __name__ == '__main__':
    with open(test_file, 'r', encoding='utf-8') as file:
        comprehend_results = json.load(file)

    #pprint(comprehend_results)

    positive_sentiment = []
    negative_sentiment = []
    for result in comprehend_results:
        if result['sentiment']['sentiment'] == 'POSITIVE':
            positive_sentiment.append(result)

        elif result['sentiment']['sentiment'] == 'NEGATIVE':
            negative_sentiment.append(result)

    print('POSITIVE RESULTS:')
    pprint(positive_sentiment)
    print('Count: ', len(positive_sentiment))

    time.sleep(1)

    positive_sentiment_sorted = sorted(positive_sentiment,
                                       key=lambda sent: sent['sentiment']['score']['Positive'],
                                       reverse=True)

    print('POSITIVE RESULTS [SORTED BY SCORE]:')
    pprint(positive_sentiment_sorted)
    print('Count: ', len(positive_sentiment_sorted))

    time.sleep(1)

    print('Removing positive results with score < ' + str(positive_score_threshold) + '.')

    for result in positive_sentiment_sorted:
        if result['sentiment']['score']['Positive'] < positive_score_threshold:
            positive_sentiment_sorted.remove(result)

    time.sleep(1)

    print('POSITIVE RESULTS [SORTED BY SCORE & THRESHOLDED]:')
    pprint(positive_sentiment_sorted)
    print('Count: ', len(positive_sentiment_sorted))

    time.sleep(1)

    print('NEGATIVE RESULTS:')
    pprint(negative_sentiment)
    print('Count: ', len(negative_sentiment))

    time.sleep(1)

    negative_sentiment_sorted = sorted(negative_sentiment,
                                       key=lambda sent: sent['sentiment']['score']['Negative'],
                                       reverse=True)

    print('NEVATIVE RESULTS [SORTED BY SCORE]:')
    pprint(negative_sentiment_sorted)
    print('Count: ', len(negative_sentiment_sorted))

    time.sleep(1)

    print('Removing negative results with score < ' + str(negative_score_threshold) + '.')

    for result in negative_sentiment_sorted:
        if result['sentiment']['score']['Negative'] < negative_score_threshold:
            negative_sentiment_sorted.remove(result)

    print('NEGATIVE RESULSTS [SORTED BY SCORE & THRESHOLDED]:')
    pprint(negative_sentiment_sorted)
    print('Count: ', len(negative_sentiment_sorted))
