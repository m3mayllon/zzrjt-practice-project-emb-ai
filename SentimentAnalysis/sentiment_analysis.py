from typing import Union
import requests
from requests.exceptions import ConnectionError, Timeout


MAX_RETRIES = 3
TIMEOUT = 10


def sentiment_analyzer(text: str, url: Union[str, None] = None, headers: Union[dict, None] = None) -> dict:
    '''This function uses Watson NLP Library to analyze sentiment from text.'''

    error_response = {'label': None, 'score': None}

    if not text:
        print('Input text cannot be empty')
        return error_response

    if not url:
        url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    if not headers:
        headers = {
            'grpc-metadata-mm-model-id': 'sentiment_aggregated-bert-workflow_lang_multi_stock'}

    for attempt in range(MAX_RETRIES):
        try:
            data = {'raw_document': {'text': text}}
            resp = requests.post(
                url, headers=headers, json=data, timeout=TIMEOUT)

            # check if the status code is not in 2XX range
            if not resp.status_code // 100 == 2:
                print(f'Unexpected status code {resp.status_code}')
                return error_response

            resp_json = resp.json()

            # parse sentiment
            label = resp_json.get('documentSentiment', {}).get('label')
            score = resp_json.get('documentSentiment', {}).get('score')

            label = label.split('_')[1]

            return {'label': label, 'score': score}

        except (ConnectionError, Timeout) as e:
            print(
                f'Connection error or timeout occurred. Retrying... ({attempt+1}/{MAX_RETRIES})')
            continue

        except Exception as exc:
            print(f'An error occurred: {exc}')
            return error_response

    print('Maximum retries exceeded. Unable to fetch sentiment.')
    return error_response
