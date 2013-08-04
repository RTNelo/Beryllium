#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    """
    The superclass of all model class. It will support some common method.
    """
    def track(self):
        """
        Add the instance to the session.
        """
        session.add(self)


Base = declarative_base(cls=BaseModel)


#Model defination.
class User(Base):
    """
    Subclass of a declarative_base that define the info structure of users.
    """

    __tablename__ = 'users'
    #The base information of an account.
    email = Column(types.String(128), primary_key=True)
    password = Column(types.String(64))
    nickname = Column(types.String(64))
    status = Column(types.Enum('host', 'admin', 'user'))
    register_time = Column(types.DateTime)

    def __init__(self,
                 email,
                 password,
                 nickname,
                 status='user',
                 register_time=None):
        """
        Need 3 strings to init.
        emial should less than 128 bits.
        password should be the literal password of an account, this method will
        convert it to the the hash value and stock it.
        nickname should less than 64 bits.
        status should be on of the ['host', 'admin', 'user'].
        register_time should be a datetime type. UTC time. Leave out it will
        use the utcnow.
        """
        self.email = email
        #Hash value converting. 3 times default.
        digest = utils.hash_repeat(password)
        self.password = digest
        self.nickname = nickname
        self.status = status
        #If datetime is None, just use the utcnow.
        self.register_time = register_time or datetime.datetime.utcnow()

    def __repr__(self):
        str_patter = ("<User('{email}', '{password}', '{nickname}', "
                      "'{status}', '{register_time}')>")
        return str_patter.format(email=self.email,
                                 password=self.password,
                                 nickname=self.nickname,
                                 status=self.status,
                                 register_time=self.register_time,
                                 )

Base.metadata.create_all(engine)


#Some alias of the session's method, please use these alias first.
def commit():
    """
    Use the commit method of the session to commit every change.
    """
    session.commit()


def rollback():
    """
    Use this to rollback.
    """
    session.rollback()
