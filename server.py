from flask import Flask, render_template, request
from nlp.sentiment import sentiment_analyzer

app = Flask('Sentiment Analyzer')


@app.route('/')
def render_index_page():
    '''
    This function initiates the rendering of the main application
    page over the Flask channel
    '''
    return render_template('index.html')


@app.route('/sentimentAnalyzer')
def sent_analyzer():
    '''
    This code receives the text from the HTML interface and 
    runs sentiment analysis over it using sentiment_analysis()
    function. The output returned shows the label and its confidence 
    score for the provided text.
    '''

    text = request.args.get('textToAnalyze')
    data = sentiment_analyzer(text)

    label = data['label']
    score = data['score']

    if not label or not score:
        return 'Invalid input! Try again.', 200

    return f'The given text has been identified as {label} with a score of {score}.', 200


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
