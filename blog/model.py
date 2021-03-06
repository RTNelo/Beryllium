#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The datamodel of the blog application.

The module will create an engine and a session according to the database
options. And It will try to create all tables if necessary. It also provide
some function like commit and rollback. Please use them first although you can
use session's method as well.
"""

import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

import markdown2

import utils
from options import options

#Prepare the engine instance.
url_pattern = 'mysql+pymysql://{user}:{pwd}@{host}/{dbname}'
url = url_pattern.format(user=options.db_user,
                         pwd=options.db_pwd,
                         host=options.db_address,
                         dbname=options.db_name,
                         )


engine = create_engine(url,
                       echo=options.debug,
                       connect_args=dict(charset='utf8')
                       )

#Prepare the session instance.
Session = sessionmaker(bind=engine)
session = Session()


#Prepare the superclass of model class.
class BaseModel(object):
    """The superclass of model class which provides some common methods."""
    def track(self):
        """Let SQLAlchemy track this object.

        This method will add the instance to the session."""
        session.add(self)

    @classmethod
    def query_filter_by(cls, **conditions):
        """Use the session to query the user with conditions.

        args:
            conditions.
        return(Query):
            The query object where you can get result of this query.
        """
        return session.query(cls).filter_by(**conditions)

    @classmethod
    def count(cls):
        """Return how many objects there are."""
        return session.query(cls).count()

    @classmethod
    def part(cls, offset, limit):
        """Offset offset and return a list having less than limit+1 object"""
        return session.query(cls).offset(offset).limit(limit).all()


Base = declarative_base(cls=BaseModel)


#Model defination.
class User(Base):
    """Subclass of a declarative_base defining the structure of users.

    Use self.articles to get a list containing the user's article object
    (ordered by the article's id).
    """

    __tablename__ = 'users'
    #The base information of an account.
    id = Column(types.Integer, primary_key=True)
    email = Column(types.String(128), unique=True, nullable=False)
    password = Column(types.String(64), nullable=False)
    nickname = Column(types.String(64), unique=True, nullable=False)
    status = Column(types.Enum('host', 'admin', 'user'), nullable=False)
    register_time = Column(types.DateTime, nullable=False)
    register_ip = Column(types.String(15), nullable=False)
    last_login_time = Column(types.DateTime, nullable=False)
    last_login_ip = Column(types.String(15), nullable=False)

    def __init__(self,
                 email,
                 password,
                 nickname,
                 register_ip,
                 last_login_time=None,
                 last_login_ip=None,
                 status='user',
                 register_time=None,
                 id=None,
                 ):
        """
        args:
            email(basestring):
                The email adress of the user. Should less than 128 bytes long.
            password(basestring):
                The raw password of the user. The __init__ method will
                calculate and store its hash value automatically. Use
                last_login_time (left out microsencond) as salt.
            nickname(basestring):
                The nickname of the user. Should less than 64 bytes long.
            register_ip(basestring):
                The ipv4 address of the user when it register the blog. Must
                be shorter than 15 bytes. str(register_ip) will be used as
                salt_suf when calculate hash value of a password.
            last_login_time(datetime.datetime,
                            default=last_login_time):
                The time when the user last login. Should be a
                UTC time too. The microsencond will be leave
                out, too.
            last_login_ip(basestring,
                          default=register_ip):
                The ip address where the user last login. Leave
                it out will use the register_ip. Must be shorter
                than 15 bytes, too.
            status(basestring, default='user'):
                The status of the user. Must be one of these values:
                    'host': the owner of the blog;
                    'admin': the administory of the blog;
                    'user': plan user of the blog.
            register_time(datetime.datetime,
                          default=datetime.datetime.utcnow):
                The time when the user register. Should be a UTC time. And
                the microsencond will be leave out. str(register_time) will be
                used as salt_pre when calculate a password hash value.
            id(int, default=auto_increase):
                The id of the user. Use None will use a new id created by
                session when commit.
        """
        self.email = email
        if len(str(email)) > 128:
            raise ValueError('email should be shorter than 128 bytes.')
        self.nickname = nickname
        if len(str(nickname)) > 64:
            raise ValueError('nickname should be shorter than 64 bytes.')
        self.register_ip = register_ip
        #If last_login_ip is None, just use self.register_ip.
        self.last_login_ip = last_login_ip or self.register_ip
        self.status = status

        #If register_time is None, just use the utcnow.
        register_time = register_time or datetime.datetime.utcnow()
        #Remove the microsencond to keep in step with data in database.
        self.register_time = utils.remove_microsecond(register_time)

        #If last_login_time is None, use self.register_time.
        last_login_time = last_login_time or self.register_time
        #Then remove the microsencond.
        self.last_login_time = utils.remove_microsecond(last_login_time)

        #Get password's hash value.
        digest = self.get_password_hash(password)
        self.password = digest

    def get_password_hash(self, password):
        """Get a password's hash value and use user's some attributes as salt.

        args:
            password(str):
                The password you want to get hash value.
        return(str):
            The hash value of the password, self.register_time as salt_pre, and
            self.register_ip as salt_suf.
        """
        #Hash value converting. 3 times default.
        digest = utils.hash_repeat(password,
                                   salt_pre=str(self.register_time),
                                   salt_suf=str(self.register_ip))
        return digest

    def __repr__(self):
        str_patter = ''.join(('<User(',
                              ', '.join(("id={id}",
                                         "email='{email}'",
                                         "password='{password}'",
                                         "nickname='{nickname}'",
                                         "status='{status}'",
                                         "register_time={register_time}",
                                         "register_ip='{register_ip}'",
                                         "last_login_time={last_login_time}",
                                         "last_login_ip='{last_login_ip}'",
                                         )),
                              ')>'))
        return str_patter.format(id=self.id,
                                 email=self.email,
                                 password=self.password,
                                 nickname=self.nickname,
                                 status=self.status,
                                 register_time=self.register_time,
                                 register_ip=self.register_ip,
                                 last_login_time=self.last_login_time,
                                 last_login_ip=self.last_login_ip,
                                 )

    @classmethod
    def get_user(cls, identification):
        """Get user by a identification.

        args:
            identification(basestring or int):
                the identification of the user you want to get. If it is a
                basestring, the method will use it as the user's email; if it
                is an int, it will be used as the user's id.
        return(User or None):
            The user you want to get. If there is no user have the
            identification return None.
        raise:
            TypeError: if identification is not an int or basestring.

        """
        if isinstance(identification, int):
            return cls.get_user_by_id(identification)
        elif isinstance(identification, basestring):
            return cls.get_user_by_email(identification)
        else:
            raise TypeError('Identification must be an int or basestring.')

    @classmethod
    def get_user_by_id(cls, id):
        """Get user by user's id.
        args:
            id(int):
                The id of user.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        return cls.query_filter_by(id=id).order_by(cls.id).first()

    @classmethod
    def get_user_by_email(cls, email):
        """Get user by user's email.
        args:
            email(basestring):
                The email of the user.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        return cls.query_filter_by(email=email).order_by(cls.id).first()

    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        """Get user by email and password.
        args:
            email(basestring):
                The user's email.
            password(basestring):
                The user's raw password. Will get it's hash value
                automatically.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        user = cls.get_user_by_email(email)
        if user is not None and (user.get_password_hash(password) ==
                                 user.password):
            return user
        else:
            return None

    @classmethod
    def have_user(cls, identification, is_nickname=False):
        """Is there a user with this identification?

        args:
            identification(int or basestring):
                The identification of the user. If it is an int, it will be
                used as the user's id. If it is a basestring, it will be used
                as the user's email if is_nickname is False, or it will be used
                as the user's nickname.
            is_nickname(bool):
                If we use identification as user's nickname When it is a
                basestring?
        return(bool):
            True if we have the user. Otherwise, return False.
        raise:
            TypeError: If identification is not an int or a basestring.
        """
        if isinstance(identification, int):
            return cls.have_user_with_id(identification)
        elif isinstance(identification, basestring):
            if is_nickname:
                return cls.have_user_with_nickname(identification)
            else:
                return cls.have_user_with_email(identification)
        else:
            raise TypeError('Identification must be an int or basestring.')

    @classmethod
    def have_user_with_id(cls, id):
        """Is there a user with this id.

        args:
            id(int):
                The id of the user.
        return(bool):
            True if we have a user with the id. Otherwise, return False.
        """
        return cls.query_filter_by(id=id).exists()

    @classmethod
    def have_user_with_email(cls, email):
        """Is there a user with this email.

        args:
            email(basestring):
                The user's email.
        return(bool):
            True if we have a user with the email. Otherwise, return False.
        """
        return cls.query_filter_by(email=email).exists()

    @classmethod
    def have_user_with_nickname(cls, nickname):
        """Is there a user with this nickname.

        args:
            nickname(basestring):
                The user's nickname.
        return(bool):
            True if we have a user with the nickname. Otherwise, return False.
        """
        return cls.query_filter_by(nickname=nickname).exists()


class Article(Base):
    """The class of a article object that defining its structure.

    Use self.author to get the user object representing the author.
    """

    __tablename__ = 'articles'

    #Base information of an article object.
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(128), unique=True, nullable=False)
    title_for_url = Column(types.String(128), unique=True, nullable=False)

    author_id = Column(types.Integer, ForeignKey('users.id'))
    #Relationship betweem user and article. Needn't init.
    author = relationship(User, backref=backref('articles', order_by=id))

    raw = Column(types.Text, nullable=True)
    content = Column(types.Text, nullable=True)
    submit_time = Column(types.DateTime, nullable=False)

    def __init__(self,
                 title,
                 title_for_url,
                 raw,
                 author=None,
                 converter=markdown2.markdown,
                 content=None,
                 submit_time=None,
                 ):
        """
        args:
            title(basestring):
                The title of the article. Must be shorter than 128 bytes.
            title_for_url(basestring):
                The title of url display. A str in ASCII encoding is
                recommended. Should be shorter than 128 bytes.
            raw(basestring):
                The raw content of the article (such as the markdown file's
                content).
            author(User, default=None):
                the author of the article. This method will add itself to the
                user's articles list automatically if author is not None.
            converter(callable):
                It's necessary if content need converting from raw. Will use
                converter(raw) to convert.
            content(basestring, default=None):
                The content of the article. If it is None, this function will
                convert the raw to content.
            submit_time(datetime.datetime, default=datetime.datetime.utcnow()):
                When the author submit the time? Should be a UTC time. If it is
                None, this method will use datetime.datetime.utcnow(). And the
                microsencond will be leave out to keep step with database.
        """
        self.title = title
        if len(str(title)) > 128:
            raise ValueError('title should be shorter than 128 bytes.')
        self.title_for_url = title_for_url
        if len(str(title_for_url)) > 128:
            raise ValueError('title_for_url should be shorter than 128 bytes.')
        self.raw = raw

        self.content = content or utils.content_convert(raw, converter)

        submit_time = submit_time or datetime.datetime.utcnow()
        self.submit_time = utils.remove_microsecond(submit_time)

        if author is not None:
            author.articles.append(self)

    def __repr__(self):
        str_patter = ''.join(('<Article(',
                              ', '.join(("id={id}",
                                         "title='{title}'",
                                         "title_for_url='{title_for_url}'",
                                         "author_id={author_id}",
                                         "submit_time={submit_time}")),
                              ')>'))
        return str_patter.format(id=self.id,
                                 title=self.title,
                                 title_for_url=self.title_for_url,
                                 author_id=self.author_id,
                                 submit_time=self.submit_time,
                                 )

    @classmethod
    def get_article(cls, identification):
        """Get user by the identification.

        Now it just is an alias of get_article_by_title_for_url.
        args:
            identification(basestring):
                The title_for_url of the article.
        return(Article or None):
            Return the Article found by the identification or None.
        """
        return cls.get_article_by_title_for_url(identification)

    @classmethod
    def get_article_by_title_for_url(cls, title_for_url):
        """Get user by the title_for_url.

        args:
            title_for_url(basestring):
                The title_for_url of the article.
        return(Article or None):
            Return the Article found by the identification or None.
        """
        return (cls.query_filter_by(title_for_url=title_for_url).
                order_by(cls.id).first())

    @classmethod
    def have_article(cls, identification):
        """Is there any article with the identification?

        This just is an alias of have_article_with_title_for_url.
        args:
            identification(basestring):
                The title_for_url.
        return(bool):
            True if have one more articles with the title_for_url, or False.
        """
        return cls.have_article_with_title_for_url(identification)

    @classmethod
    def have_article_with_title_for_url(cls, title_for_url):
        """Is there any article with the title for url?

        args:
            title_for_url(basestring):
                The title_for_url.
        return(bool):
            True if have one or more article with the title_for_url, or False.
        """
        return cls.query_filter_by(title_for_url=title_for_url).exists()


class Comment(Base):
    """Class of a comment."""
    __tablename__ = 'comments'

    #Base information of a comment.
    id = Column(types.Integer, primary_key=True)

    author_id = Column(types.Integer, ForeignKey('users.id'))
    #Relationship betweem Comment and User.
    author = relationship(User, backref=backref('comments', order_by=id))

    raw = Column(types.Text, nullable=False)
    content = Column(types.Text, nullable=False)
    submit_time = Column(types.DateTime, nullable=False)

    article_id = Column(types.Integer, ForeignKey('articles.id'))
    #Relationship betweem Comment and Article.
    article = relationship(Article, backref=backref('comments', order_by=id))

    def __init__(self,
                 raw,
                 author=None,
                 article=None,
                 converter=markdown2.markdown,
                 content=None,
                 submit_time=None,
                 id=None,
                 ):
        """
        args:
            raw(basestring):
                Raw content of the Comment. Such as the markdown file's
                content.
            content(basestring):
                The content displayed for visitor. If it is None, __init__ will
                convert the raw and use the result as the content
                automatically.
            author(User, default=None):
                The author of the comment. If it is not None, __init__ will
                append the comment to author's comments attribute.
            article(Article, default=None):
                The article which own this comment. __init__ will append the
                comment to article.comments if article is not None.
            converter(callable):
                It's necessary if content need converting from raw. Will use
                converter(raw) to convert.
            submit_time(datetime.datetime, default=datetime.datetime.utcnow():
                The UTC time when author submit the comment. If it is None, use
                datetime.datetime.utcnow() as default. Then the microsencond
                will be leave out to keep step with database.
            id(int, default=None):
                The id of the comment. If it is None, will use a value
                presented by database.
        """
        self.raw = raw
        self.content = content or utils.content_convert(self.raw, converter)
        submit_time = submit_time or datetime.datetime.utcnow()
        self.submit_time = utils.remove_microsecond(submit_time)
        if id is not None:
            self.id = id
        if author is not None:
            author.comments.append(self)
        if article is not None:
            article.comments.append(self)

    def __repr__(self):
        str_patter = ''.join(('<Comment(',
                              ', '.join(("id={id}",
                                         "author_id={author_id}",
                                         "article_id={article_id}",
                                         "submit_time={submit_time}")),
                              ')>'))
        return str_patter.format(id=self.id,
                                 author_id=self.author_id,
                                 article_id=self.article_id,
                                 submit_time=self.submit_time,
                                 )


Base.metadata.create_all(engine)


#Some alias of the session's method, please use these alias first.
def commit():
    """Use the commit method of the session to commit every change."""
    session.commit()


def rollback():
    """Use this to rollback."""
    session.rollback()
