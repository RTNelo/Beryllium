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

engine = create_engine(url, echo=options.debug)

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
            email(str): the email adress of the user. Should less than 128
                        bytes long.
            password(str): the raw password of the user. The __init__ method
                           will calculate and store its hash value
                           automatically. Use last_login_time (left out
                           microsencond) as salt.
            nickname(str): the nickname of the user. Should less than 64 bytes
                           long.
            register_ip(str): the ipv4 address of the user when it register the
                              blog. Must be shorter than 15 bytes.
                              str(register_ip) will be used as salt_suf when
                              calculate hash value of a password.
            last_login_time(datetime.datetime,
                            default=last_login_time):
                                the time when the user last login. Should be a
                                UTC time too. The microsencond will be leave
                                out, too.
            last_login_ip(str,
                          default=register_ip):
                              the ip address where the user last login. Leave
                              it out will use the register_ip. Must be shorter
                              than 15 bytes, too.
            status(str, default='user'): the status of the user. Must be one
                                         of these values:
                             'host': the owner of the blog;
                             'admin': the administory of the blog;
                             'user': plan user of the blog.
            register_time(datetime.datetime,
                          default=datetime.datetime.utcnow):
                              the time when the user register. Should be a UTC
                              time. And the microsencond will be leave out.
                              str(register_time) will be used as salt_pre when
                              calculate a password hash value.
            id(int, default=auto_increase): the id of the user. Use None will
                                            use a new id created by session
                                            when commit.
        """
        self.email = email
        self.nickname = nickname
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
            password(str): the password you want to get hash value.
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

    @staticmethod
    def get_user(identification):
        """Get user by a identification.

        args:
            identification(str or int): the identification of the user you want
                                        to get. If it is str, the method will
                                        use it as the user's email; if it is
                                        int, it will be used as the user's id.
        return(User or None):
            The user you want to get. If there is no user have the
            identification return None.
        raise:
            TypeError: if identification is not an int or str.

        """
        if isinstance(identification, int):
            return User.get_user_by_id(identification)
        elif isinstance(identification, str):
            return User.get_user_by_email(identification)
        else:
            raise TypeError('Identification must be an int or string.')

    @staticmethod
    def get_user_by_id(id):
        """Get user by user's id.
        args:
            id(int): the id of user.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        return User._query_filter_by(id=id).order_by(User.id).first()

    @staticmethod
    def get_user_by_email(email):
        """Get user by user's email.
        args:
            email(str): the email of the user.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        return User._query_filter_by(email=email).order_by(User.id).first()

    @staticmethod
    def get_user_by_email_and_password(email, password):
        """Get user by email and password.
        args:
            email(str): the user's email.
            password(str): the user's raw password. Will get it's hash value
                           automatically.
        return(User or None):
            The first user (ordered by id) meet the condition. Or None if no
            user have the email.
        """
        user = User.get_user_by_email(email)
        if user is not None and (user.get_password_hash(password) ==
                                 user.password):
            return user
        else:
            return None

    @staticmethod
    def have_user(identification, is_nickname=False):
        """Is there a user with this identification?

        args:
            identification(int or str): the identification of the user. If it
                                        is an int, it will be used as the
                                        user's id. If it is a str, it will be
                                        used as the user's email if is_nickname
                                        is False, or it will be used as the
                                        user's nickname.
            is_nickname(bool): if we use identification as user's nickname When
                               it is a str?
        return(bool):
            True if we have the user. Otherwise, return False.
        raise:
            TypeError: If identification is not an int or a string.
        """
        if isinstance(identification, int):
            return User.have_user_with_id(identification)
        elif isinstance(identification, str):
            if is_nickname:
                return User.have_user_with_nickname(identification)
            else:
                return User.have_user_with_email(identification)
        else:
            raise TypeError('Identification must be an int or string.')

    @staticmethod
    def have_user_with_id(id):
        """Is there a user with this id.

        args:
            id(int): the id of the user.
        return(bool):
            True if we have a user with the id. Otherwise, return False.
        """
        count = User._query_filter_by(id=id).count()
        return count > 0

    @staticmethod
    def have_user_with_email(email):
        """Is there a user with this email.

        args:
            email(str): the user's email.
        return(bool):
            True if we have a user with the email. Otherwise, return False.
        """
        count = User._query_filter_by(email=email).count()
        return count > 0

    @staticmethod
    def have_user_with_nickname(nickname):
        """Is there a user with this nickname.

        args:
            nickname(str): the user's nickname.
        return(bool):
            True if we have a user with the nickname. Otherwise, return False.
        """
        count = User._query_filter_by(nickname=nickname).count()
        return count > 0

    @staticmethod
    def _query_filter_by(**conditions):
        """Use the session to query the user with conditions.

        args:
            conditions.
        return(Query):
            The query object where you can get result of this query.
        """
        return session.query(User).filter_by(**conditions)


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
            title(str): the title of the article. Must be shorter than 128
                        bytes.
            title_for_url(str): the title of url display. A string in ASCII
                                encoding is recommended. Should be shorter
                                than 128 bytes.
            raw(str): the raw content of the article (such as the markdown
                      file's content).
            author(User, default=None): the author of the article. This method
                          will add itself to the user's articles list
                          automatically if author is not None.
            converter(callable): It's necessary if content need converting
                                 from raw. Will use converter(raw) to convert.
            content(str, default=None): the content of the article. If it is
                          None, this function will convert the raw to content.
            submit_time(datetime.datetime, default=datetime.datetime.utcnow()):
                    When the author submit the time? Should be a UTC time. If
                    it is None, this method will use datetime.datetime.utcnow()
                    And the microsencond will be leave out to keep step with
                    database.
        """
        self.title = title
        self.title_for_url = title
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
            raw(str): raw content of the Comment. Such as the markdown file's
                      content.
            content(str): the content displayed for visitor. If it is None,
                          __init__ will convert the raw and use the result as
                          the content automatically.
            author(User, default=None): the author of the comment. If it is not
                                        None, __init__ will append the comment
                                        to author's comments attribute.
            article(Article, default=None): the article which own this comment.
                                            __init__ will append the comment to
                                            article.comments if article is not
                                            None.
            converter(callable): It's necessary if content need converting
                                 from raw. Will use converter(raw) to convert.
            submit_time(datetime.datetime, default=datetime.datetime.utcnow():
                    The UTC time when author submit the comment. If it is None,
                    use datetime.datetime.utcnow() as default. Then the
                    microsencond will be leave out to keep step with database.
            id(int, default=None): the id of the comment. If it is None, will
                                   use a value presented by database.
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
