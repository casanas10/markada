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
from flask_cors import cross_origin


Bootstrap(app)


class LinkForm(Form):
    link = StringField("")
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

        try:
            article = Article(link)
            article.download()
            article.parse()

            sentiment = sentiment_analysis(article.text)
            authors = ",".join(article.authors)
        except:

            flash("Article URL is invalid. Please try again", "error")
            return render_template('index.html', form=form)

        resp = {
            "sentiment": str(sentiment),
            "headline": str(article.title),
            "content": str(article.text),
            "publishedDate": str(article.publish_date),
            "authors": str(authors),
            "url": str(link),
        }

        json_res = json.dumps(resp, indent=4)

        return render_template('index.html', form=form, resp=resp, json_res=json_res)

    return render_template('index.html', form=form)

@cross_origin()
@app.route("/v1/news/")
def news_sentiment_analysis():

    link = request.args.get('url')

    try:
        article = Article(link)
        article.download()
        article.parse()

        sentiment = sentiment_analysis(article.text)
        authors = ",".join(article.authors)

    except:

        resp = {
            "response": "BAD-REQUEST. Could not parse the article. Try another article or check the URL"
        }
        return jsonify(resp), 404



    flash("Sentiment: " + str(sentiment))
    flash("Headline: " + str(article.title))
    flash("Article Content: " + str(article.text))
    flash("Published Date: " + str(article.publish_date))
    flash("Authors: " + str(authors))
    flash("url: " + str(link))

    resp = {
        "sentiment": str(sentiment),
        "headline": str(article.title),
        "content": str(article.text),
        "publishedDate": str(article.publish_date),
        "authors": str(article.authors),
        "url": str(link)
    }

    return jsonify(resp), 200

@app.route("/news")
def show_news():
    news = models.Article.query.all()
    return render_template('news.html', news=news)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def stringify(response_string):
    response = ''
    for word in response_string.split():
        new_word = word
        if word == 'true':
            new_word = '\"true\"'
        if word == 'false':
            new_word = '\"false\"'
        if word == 'none':
            new_word = '\"none\"'
        if word == 'true,':
            new_word = '\"true\",'
        if word == 'false,':
            new_word = '\"false\",'
        if word == 'none,':
            new_word = '\"none\",'
        response += (new_word + ' ')
    return response