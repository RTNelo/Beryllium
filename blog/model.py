#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker

from options import options

#Prepare the engine instance.
url_pattern = 'mysql+pymysql://{user}:{pwd}@{host}/{dbname}'
url = url_pattern.format(user=options.db_user,
                         pwd=options.db_pwd,
                         host=options.db_address,
                         dbname=options.db_name,
                         )

engine = create_engine(url)

#Prepare the session instance.
Session = sessionmaker(bind=engine)
session = Session()

#Prepare the superclass of model class.
Base = declarative_base()


class User(Base):
    """
    Subclass of a declarative_base that define the info structure of users.
    """

    __tablename__ = 'users'
    #The base information of an account.
    email = Column(String(128), primary_key=True)
    password = Column(String(64))
    nickname = Column(String(64))

    def __init__(self, email, password, nickname):
        """
        Need 3 strings to init.
        emial should less than 128 bits.
        password should be the literal password of an account, this method will
        convert it to the the hash value and stock it.
        nickname should less than 64 bits.
        """
        self.email = email
        #TODO: Hash value converting.
        self.password = password
        self.nickname = nickname

    def __repr__(self):
        str_patter = "<User('{email}', '{password}', '{nickname}')>"
        return str_patter.format(email=self.email,
                                 password=self.password,
                                 nickname=self.nickname,
                                 )

Base.metadata.create_all(engine)
