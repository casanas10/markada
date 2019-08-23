from api import db, ma
from sqlalchemy import Column, Integer, String, Date, TEXT
import datetime

db.create_all()

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    email = Column(String(255), unique=True)
    password = Column(String(80))

    def __repr__(self):
        return '<user %r>' % self.email

class Article(db.Model):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    author = Column(String(255))
    publishedDate = Column(Date, default=datetime.datetime.now())
    article_title = Column(TEXT)
    article_content = Column(TEXT)

    def __repr__(self):
        return 'article %r>' % self.article_title

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'publishedDate', 'article_title', 'article_content')

user_schema = UserSchema() # if you are expecting 1 record back
users_schema = UserSchema(many=True) #if expecting many records back

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)