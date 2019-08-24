from flask import render_template, request, flash
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from api import app, db, models


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


Bootstrap(app)


class LinkForm(Form):
    link = TextField("Link:")


stopwords = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text

def sentiment_analysis(x):

    #string to array
    # x_array = [x]
    # print(x_array)

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

    # #transform words into vector of features
    # tfidf_vect = TfidfVectorizer(analyzer=clean_text)
    # tfidf_vect_fit = tfidf_vect.fit(x_array)
    #
    # vect = tfidf_vect_fit.transform(x_array)
    # y = pd.DataFrame(vect.toarray())

    # vect = vectorizer.fit_transform(x_array).toarray()

    # df = pd.DataFrame(X, columns=vectorizer.get_feature_names())

    #predict sentiment
    # print(model.predict(y))



@app.route("/", methods=["GET", "POST"])
def index():

    form = LinkForm(request.form)
    if request.method == 'POST':
        link = request.form['link']
        print(link)

        article = Article(link)
        article.download()
        article.parse()

        print("-------")
        print(article.title)
        print(article.text)
        print(article.publish_date)
        print(article.authors)

        sentiment_analysis(article.title)

        flash("This is the link:" + link)
    return render_template('index.html', form=form)

@app.route("/news")
def show_news():
    news = models.Article.query.all()
    return render_template('news.html', news=news)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404