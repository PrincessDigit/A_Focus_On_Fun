import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
class languager:
    def __init__(self):
        pass

    def process_text(self, text):
        # text = text.replace(",", "")
        # text = text.replace("|", "")
        # text = text.replace(".", "")
        # tokens = word_tokenize(text)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        stop_words = set(stopwords.words('english'))

        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        counts = Counter(filtered_tokens)
        counts_l = sorted(list(counts.values()), reverse=True)
        dic = self.sort_words(counts)
        return scores, dic

    def sort_words(self, count):
        sorted_dict = {}
        sorted_dict = dict(sorted(count.items(), key = lambda item: item[1], reverse=True))
        return sorted_dict
    
    