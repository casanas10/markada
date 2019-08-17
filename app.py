import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date, TEXT
import os
import config
import datetime

app = flask.Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + config.dbConfig["user"] + ":"+ config.dbConfig["password"] +"@"+ config.dbConfig["host"]+"/articles"
# engine = create_engine("mysql+mysqldb://" + config.dbConfig["user"] + ":"+ config.dbConfig["password"] +"@"+ config.dbConfig["host"]+"/articles")
# connection = engine.connect()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.config["DEBUG"] = True


#Creating the database
@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created!")

@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped!")

@app.cli.command("db_seed")
def db_seed():
    apple_news = Article(author="John Doe",
                         publishedDate="2019-02-22",
                         article_title="Apple announces news subscription service, Apple News+",
                         article_content="""Apple News is getting into the subscription business. 
At Monday's Apple event at the Steve Jobs Theater in Cupertino, the company announced a new subscription service called Apple News Plus (or, Apple News+). 
Tim Cook positioned the service as a way to get access to magazines — as opposed to just articles from news outlets — with just one subscription. Pay $9.99 a month and you'll get access to over 300 magazines covering topics like entertainment, news, fashion, and more.
"I miss the feeling of being at the newsstand," Tim Cook said, seemingly forgetting that Apple devices helped make buying physical magazines obsolete.Apple News+ is launching with a host of heavy hitters in media. Condé Nast, which publishes Vogue, The New Yorker, Wired, and more, is on board, as are the Los Angeles Times and the Wall Street Journal. 
"We've got magazines for just about every passion under the sun, and Apple News+  is the only place where you will find all of these magazines in the same place," Roger Rosner, Apple's VP of applications, said.""")

    ibm_news = Article(author="Nemo Doe",
                       publishedDate="2019-08-16",
                       article_title="Why Is IBM (IBM) Down 11.8% Since Last Earnings Report?",
                       article_content="""It has been about a month since the last earnings report for IBM (IBM). Shares have lost about 11.8% in that time frame, underperforming the S&P 500.

Will the recent negative trend continue leading up to its next earnings release, or is IBM due for a breakout? Before we dive into how investors and analysts have reacted as of late, let's take a quick look at the most recent earnings report in order to get a better handle on the important drivers.
IBM Surpasses Q2 Earnings & Revenue Estimates, Acquires Red Hat
IBM delivered second-quarter 2019 non-GAAP earnings of $3.17 per share, which surpassed the Zacks Consensus Estimate of $3.06. Further, earnings per share (EPS) increased 9 cents from the year-ago quarte
Revenues of $19.16 billion outpaced the Zacks Consensus Estimate of $19.11 billion but declined 4.2% on a year-over-year basis. At constant currency (cc), the metric dipped 1.6%. The year-over-year revenue decline can primarily be attributed to currency fluctuation and headwinds from IBM Z product cycle.
Notably, IBM stated that signings declined 14% on cc basis in the second quarter to $9.7 billion. Services backlog fell 4% year over year and totaled $111.2 billion.""")

    db.session.add(apple_news)
    db.session.add(ibm_news)

    test_user = User(first_name="Alex",
                     last_name="Casanas",
                     email="test@test.com",
                     password="password")

    db.session.add(test_user)
    db.session.commit()
    print("Database seeded!")

@app.route('/', methods=['GET'])
def home():
    return jsonify(message="<h1> Return Me!!</h1>")

@app.route('/v1/news', methods=['GET'])
def get_all_news():

    query_params = request.args
    from_param = query_params.get('from')
    to_param = query_params.get('to')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if from_param:
        query += ' from=? AND'
        to_filter.append(from_param)
    if to_param:
        query += ' to=? AND'
        to_filter.append(to_param)

    if not (from_param or to_param):
        return page_not_found(404)

    query = query[:-4] + ';'

    print(query)
    print(to_filter)

    return "ALL NEWS PLEASE"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Page Not Found</p>", 404


#database models
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    email = Column(String(255), unique=True)
    password = Column(String(80))

class Article(db.Model):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    author = Column(String(255))
    publishedDate = Column(Date, default=datetime.datetime.now())
    article_title = Column(TEXT)
    article_content = Column(TEXT)


if __name__ == "__main__":

    app.run()




