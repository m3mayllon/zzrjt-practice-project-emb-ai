from typing import Union
import requests
from requests.exceptions import ConnectionError, Timeout


MAX_RETRIES = 3
TIMEOUT = 10


def sentiment_analyzer(text: str, url: Union[str, None] = None, headers: Union[dict, None] = None) -> dict:

    error_response = {'label': None, 'score': None}

    if not url:
        url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    if not headers:
        headers = {
            'grpc-metadata-mm-model-id': 'sentiment_aggregated-bert-workflow_lang_multi_stock'}

    for attempt in range(MAX_RETRIES):
        try:
            data = {'raw_document': {'text': text}}

            resp = requests.post(url, headers=headers, json=data, timeout=10)
            resp.raise_for_status()

            resp_json = resp.json()

            label = resp_json.get('documentSentiment', {}).get('label')
            score = resp_json.get('documentSentiment', {}).get('score')

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
