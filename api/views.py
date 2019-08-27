from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired
from api import app, db, models
import json

import pandas as pd
from newspaper import Article
import pickle
from sklearn.externals import joblib


Bootstrap(app)


class LinkForm(Form):
    link = StringField("Enter an article link:", validators=[DataRequired()])
    submit = SubmitField('Submit')


def sentiment_analysis(x):

    # load the model from disk
    # Load from file
    with open("api/data/rf_model.pkl", 'rb') as file:
        rf_model = pickle.load(file)

    tfidfVectorizer = joblib.load('api/data/tfidfVectorizer.pkl')

    tfidf_train = tfidfVectorizer.transform([x])
    x = pd.DataFrame(tfidf_train.toarray())

    return rf_model.predict(x)[0]


@app.route("/", methods=["GET", "POST"])
def index():

    form = LinkForm(request.form)
    if request.method == 'POST' and form.validate():

        link = request.form['link']

        article = Article(link)
        article.download()
        article.parse()

        sentiment = sentiment_analysis(article.title)

        flash("Sentiment: " + str(sentiment))
        flash("Headline: " + str(article.title))
        flash("Article Content: " + str(article.text))
        flash("Published Date: " + str(article.publish_date))
        flash("Authors: " + str(article.authors))
        flash("url: " + str(link))

        resp = {
            "sentiment": str(sentiment),
            "headline": str(article.title),
            "content": str(article.text),
            "publishedDate": str(article.publish_date),
            "authors": str(article.authors),
            "url": str(link)
        }

        flash("JSON Response: " + str(resp))

        return redirect(url_for('index'))

    return render_template('index.html', form=form)

@app.route("/v1/news/")
def news_sentiment_analysis():

    link = request.args.get('url')

    article = Article(link)
    article.download()
    article.parse()

    sentiment = sentiment_analysis(article.title)

    flash("Sentiment: " + str(sentiment))
    flash("Headline: " + str(article.title))
    flash("Article Content: " + str(article.text))
    flash("Published Date: " + str(article.publish_date))
    flash("Authors: " + str(article.authors))
    flash("url: " + str(link))

    resp = {
        "sentiment": str(sentiment),
        "headline": str(article.title),
        "content": str(article.text),
        "publishedDate": str(article.publish_date),
        "authors": str(article.authors),
        "url": str(link)
    }

    return jsonify(resp)


@app.route("/news")
def show_news():
    news = models.Article.query.all()
    return render_template('news.html', news=news)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404