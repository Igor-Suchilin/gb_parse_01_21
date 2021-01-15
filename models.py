from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table


Base = declarative_base()

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, unique=False, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author")
    tags = relationship('Tag', secondary=tag_post)

# class Comment(Base):
#     __tablename__ = 'comment'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     url = Column(String, unique=True, nullable=False)
#     body = Column(String, unique=False)
#     posts_id = Column(Integer, ForeignKey('posts.id'))
#     writer_id = Column(Integer, ForeignKey('writer.id'))
#     writer = relationship("Writer")
#     posts = relationship("Post")

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False)
    posts = relationship("Post")

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    posts = relationship("Post", secondary=tag_post)

# class Writer(Base):
#     __tablename__ = 'writer'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     url = Column(String, unique=True, nullable=False)
#     name = Column(String, unique=False)
