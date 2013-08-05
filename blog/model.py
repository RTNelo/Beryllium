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
from sqlalchemy.orm import sessionmaker

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
    """Subclass of a declarative_base defining the structure of users."""

    __tablename__ = 'users'
    #The base information of an account.
    id = Column(types.Integer, primary_key=True)
    email = Column(types.String(128), unique=True, nullable=False)
    password = Column(types.String(64), nullable=False)
    nickname = Column(types.String(64), nullable=False)
    status = Column(types.Enum('host', 'admin', 'user'), nullable=False)
    register_time = Column(types.DateTime, nullable=False)
    last_login_time = Column(types.DateTime, nullable=False)

    def __init__(self,
                 email,
                 password,
                 nickname,
                 status='user',
                 id=None,
                 register_time=None,
                 last_login_time=None):
        """
        args:
            email(str): the email adress of the user. Should less than 128 bits
                        long.
            password(str): the raw password of the user. The __init__ method
                           will calculate and store its hash value
                           automatically.
            nickname(str): the nickname of the user. Should less than 64 bits
                           long.
            status(str): the status of the user. Must be one of these values:
                             'host': the owner of the blog;
                             'admin': the administory of the blog;
                             'user': plan user of the blog.
            id(int, default=auto_increase): the id of the user. Use None will
                                            use a new id created by session
                                            when commit.
            register_time(datetime.datetime,
                          default=datetime.datetime.utcnow):
                              the time when the user register. Should be a UTC
                              time. And the microsencond will be leave out.
            last_login_time(datetime.datetime,
                            default=last_login_time):
                                the time when the user last login. Should be a
                                UTC time too. The microsencond will be leave
                                out, too.
        """
        self.email = email
        self.nickname = nickname
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
        digest = self.get_password_digest(password)
        self.password = digest

    def get_password_digest(self, password):
        """Get a password's hash value that self.register_time as salt_pre.

        args:
            password(str): the password you want to get hash value.
        return(str):
            The hash value of the password, self.register_time as salt_pre.
        """
        #Hash value converting. 3 times default. Use register_time as salt_pre.
        digest = utils.hash_repeat(password, salt_pre=str(self.register_time))
        return digest

    def __repr__(self):
        str_patter = ("<User({id}, '{email}', '{password}', '{nickname}', "
                      "'{status}', '{register_time}', '{last_login_time}')>")
        return str_patter.format(id=self.id,
                                 email=self.email,
                                 password=self.password,
                                 nickname=self.nickname,
                                 status=self.status,
                                 register_time=self.register_time,
                                 last_login_time=self.last_login_time,
                                 )

Base.metadata.create_all(engine)


#Some alias of the session's method, please use these alias first.
def commit():
    """Use the commit method of the session to commit every change."""
    session.commit()


def rollback():
    """Use this to rollback."""
    session.rollback()
