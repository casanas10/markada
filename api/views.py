from flask import render_template
from flask_bootstrap import Bootstrap
from api import app, db, models

Bootstrap(app)

@app.route("/news")
def show_news():
    news = models.Article.query.all()
    return render_template('news.html', news=news)
