from typing import Union
import requests
from requests.exceptions import ConnectionError, Timeout

MAX_RETRIES = 3
TIMEOUT = 10


def emotion_detector(text_to_analyze: str, url: Union[str, None] = None, headers: Union[dict, None] = None) -> str:
    '''This function uses Watson NLP Library to detect emotion from text.'''

    error_response = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    if not text_to_analyze:
        print('Input text cannot be empty')
        return error_response

    if not url:
        url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    if not headers:
        headers = {
            'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'}

    for attempt in range(MAX_RETRIES):
        try:
            data = {'raw_document': {'text': text_to_analyze}}
            resp = requests.post(url, headers=headers,
                                 json=data, timeout=TIMEOUT)

            # check if the status code is not in 2XX range
            if not resp.status_code // 100 == 2:
                print(f'Unexpected status code {resp.status_code}')
                return error_response

            resp_json = resp.json()

            # parse emotions
            emotions = resp_json.get('emotionPredictions', {})[
                0].get('emotion', {})
            emotions['dominant_emotion'] = max(emotions, key=emotions.get)

            return emotions

        except (ConnectionError, Timeout) as e:
            print(
                f'Connection error or timeout occurred. Retrying... ({attempt+1}/{MAX_RETRIES})')
            continue

        except Exception as exc:
            print(f'An error occurred: {exc}')
            return error_response

    print('Maximum retries exceeded. Unable to fetch sentiment.')
    return error_response
