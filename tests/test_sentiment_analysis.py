import unittest
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer


class TestSentimentAnalysis(unittest.TestCase):

    test_cases = [
        ('I am glad this happened', 'POSITIVE'),
        ('I am really mad about this', 'NEGATIVE'),
        ('I feel disgusted just hearing about this', 'NEGATIVE'),
        ('I am so sad about this', 'NEGATIVE'),
        ('I am really afraid that this will happen', 'NEGATIVE')
    ]

    def test_sentiment_analyzer(self):
        for text, expected_sentiment in self.test_cases:
            with self.subTest(text=text):
                result = sentiment_analyzer(text)
                self.assertEqual(result['label'], expected_sentiment)


if __name__ == '__main__':

    unittest.main()
