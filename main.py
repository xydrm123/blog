#!/bin/bash
#-*-codinng:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

class User(db.Model):
    """Blog User Table"""

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref = 'user',
        lazy = 'dynamic'
    )

    def __init__(self,username):
        self.username = username

    def __repr__(self):
        return "<'{}'>".format(self.username)

tags = db.Table('post_tags',
                db.Column('post_id',db.Integer(),db.ForeignKey('post.id')),
                db.Column('tag_id',db.Integer(),db.ForeignKey('tag.id')),
            )

class Post(db.Model):
    """Blog Artical Table"""

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    pub_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comments',
        backref = 'post',
        lazy = 'dynamic'
    )
    tags = db.relationship(
        'Tags',
        secondary = tags,
        backref = db.backref('posts', lazy='dynamic')
    )
    def __init__(self,title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Comments(db.Model):
    """Blog Comments Table"""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])




class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
if __name__ == '__main__':
    app.run()
