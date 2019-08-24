import pandas as pd
import numpy as np
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.python.keras.models import load_model
from newspaper import Article
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tensorflow.python.keras.preprocessing.text import Tokenizer
import pickle

stopwords = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text

if __name__=="__main__":
    # x_data = []
    #
    # x_data.append("I am a little confused on all of the models of the 88-89 bonnevilles")
    #
    # # load tokenizer
    # tokenizer = Tokenizer()
    # with open('data/tokenizer.pickle', 'rb') as handle:
    #     tokenizer = pickle.load(handle)
    #
    # x_data_series = pd.Series(x_data)
    # x_tokenized = tokenizer.texts_to_matrix(x_data_series, mode='tfidf')
    #
    # model = load_model('data/my_model.h5')
    #
    # labels = np.array(['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
    #                    'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
    #                    'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
    #                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
    #                    'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast',
    #                    'talk.politics.misc', 'talk.religion.misc'])
    #
    # i = 0
    # for x_t in x_tokenized:
    #     prediction = model.predict(np.array([x_t]))
    #     predicted_label = labels[np.argmax(prediction[0])]
    #     print("Predicted label: " + predicted_label)
    #     i += 1

    # #load the model
    model = load_model('data/model.h5')

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    x = [
        'March 15 (Reuters) - Mobile phone chip supplier Qualcomm Inc on Friday won a court victory against iPhone maker Apple Inc, with a jury in federal court in San Diego finding that Apple infringed on three of Qualcomm’s patents, a Qualcomm spokeswoman told Reuters. (Reporting by Stephen Nellis; Editing by Richard Chang)']

    vectorizer = TfidfVectorizer(analyzer=clean_text)
    vectorizer = vectorizer.fit(x)

    # load tokenizer
    with open('data/tfidf_vect_fit.pickle', 'rb') as handle:
        tfidf_vect_fit = pickle.load(handle)

    tfidf_train = tfidf_vect_fit.transform(x)
    x = pd.DataFrame(tfidf_train.toarray())

    print(model.predict(x))