'''This module runs Flask web framework on debug mode.'''

from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask('')


@app.route('/')
def render_index_page():
    '''
    This function initiates the rendering of the main application
    page over the Flask channel
    '''
    return render_template('index.html')


@app.route('/sentimentAnalyzer')
def analyze_sentiment():
    '''
    This funtion receives a text from the HTML interface and runs sentiment_analyzer() function.
    The output shows provided text sentiment scores detected.
    '''

    data = sentiment_analyzer(request.args.get('textToAnalyze'))

    label = data['label']
    score = data['score']

    if not label or not score:
        return 'Invalid text! Please try again!'

    return f'The given text has been identified as {label} with a score of {score}.'


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
