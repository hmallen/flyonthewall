import boto3
import json
import logging
from pprint import pprint
import sys
import time

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

test_phrase = 'It is raining today in Seattle.'


def get_entities(input_text):
    comprehend_results = comprehend_client.detect_entities(Text=input_text, LanguageCode='en')

    entities = comprehend_results['Entities']
    metadata = comprehend_results['ResponseMetadata']

    return entities, metadata


def get_key_phrases(input_text):
    comprehend_results = comprehend_client.detect_key_phrases(Text=input_text, LanguageCode='en')

    key_phrases = comprehend_results['KeyPhrases']
    metadata = comprehend_results['ResponseMetadata']

    return key_phrases, metadata


def get_sentiment(input_text):
    comprehend_results = comprehend_client.detect_sentiment(Text=input_text, LanguageCode='en')

    sentiment = {'sentiment': comprehend_results['Sentiment'], 'score': comprehend_results['SentimentScore']}
    metadata = comprehend_results['ResponseMetadata']

    return sentiment, metadata


if __name__ == '__main__':
    try:
        comprehend_client = boto3.client(service_name='comprehend',
                                         region_name='us-east-1')

        entities, entities_metadata = get_entities(test_phrase)

        for entity in entities:
            print(entity['Type'], entity['Text'])

        #pprint(entities_metadata)

        key_phrases, key_phrases_metadata = get_key_phrases(test_phrase)

        for phrase in key_phrases:
            print(phrase['Score'], phrase['Text'])

        #pprint(key_phrases_metadata)

        sentiment, sentiment_metadata = get_sentiment(test_phrase)

        print('Sentiment: ', sentiment['sentiment'])

        for category in sentiment['score']:
            print(category, sentiment['score'][category], type(sentiment['score'][category]))

        #pprint(sentiment_metadata)
        
    except Exception as e:
        logger.exception('Exception encountered.')
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')

        sys.exit()
