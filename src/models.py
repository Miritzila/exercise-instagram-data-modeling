import os
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='author')
    following = relationship('Follower', foreign_keys=('Follower.user_from_id'), backref='follower')
    followers = relationship('Follower', foreign_keys=('Follower.user_to_id'), backref='user')

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed = relationship('User', foreign_keys=('Follower.user_from_id'), backref='followers')
    follower = relationship('User', foreign_keys=('Follower.user_to_id'), backref='following')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='posts')
    media = relationship('Media', backref='post')
    comments = relationship('Comment', backref='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum)
    url = Column(String)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', backref='media')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    author = relationship('User', backref='comments')
    post = relationship('Post', backref='comments')

    def to_dict(self):
        return {}

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e