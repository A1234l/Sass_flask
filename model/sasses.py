""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Sass(db.Model):
    __tablename__ = 'sasses'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=False, nullable=False)
    _question1 = db.Column(db.String(255), unique=False, nullable=False)
    _question2 = db.Column(db.String(255), unique=False, nullable=False)
    _question3 = db.Column(db.String(255), unique=False, nullable=False)
    _question4 = db.Column(db.String(255), unique=False, nullable=False)
    _doquestion = db.Column(db.Date)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, username, question1, question2, question3, question4, doquestion=date.today()):
        self._username = username    # variables with self prefix become part of the object, 
        self._question1 = question1
        self._question2 = question2
        self._question3 = question3
        self._question4 = question4
        self._doquestion = doquestion

    # a name getter method, extracts name from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows name to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username

    # a name getter method, extracts name from object
    @property
    def question1(self):
        return self._question1
    
    # a setter function, allows name to be updated after initial object creation
    @question1.setter
    def question1(self, question1):
        self._question1 = question1

        # a name getter method, extracts name from object
    @property
    def question2(self):
        return self._question2
    
    # a setter function, allows name to be updated after initial object creation
    @question2.setter
    def question2(self, question2):
        self._question2 = question2

        # a name getter method, extracts name from object
    @property
    def question3(self):
        return self._question3
    
    # a setter function, allows name to be updated after initial object creation
    @question3.setter
    def question3(self, question3):
        self._question3 = question3

        # a name getter method, extracts name from object
    @property
    def question4(self):
        return self._question4
    
    # a setter function, allows name to be updated after initial object creation
    @question4.setter
    def question4(self, question4):
        self._question4 = question4
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def doquestion(self):
        doquestion_string = self._doquestion.strftime('%m-%d-%Y')
        return doquestion_string
    
    # dob should be have verification for type date
    @doquestion.setter
    def doquestion(self, doquestion):
        self._doquestion = doquestion
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
            "doquestion": self.doquestion
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, username="", question1="", question2="", question3="", question4=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(question1) > 0:
            self.question1 = question1
        if len(question2) > 0:
            self.question2 = question2
        if len(question3) > 0:
            self.question3 = question3
        if len(question4) > 0:
            self.question4 = question4
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initSasses():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = Sass(username='Bob', question1='hi', question2='test', question3='no you', question4='I dont know',doquestion=date(1945, 9, 2))
        u2 = Sass(username='Jeff', question1='hello', question2='help I dont know', question3='answer is 1', question4='this is so hard',doquestion=date(2020, 5, 15))
        u3 = Sass(username='Test', question1='testing', question2='more testing', question3='even more testing', question4='the final testing',doquestion=date(2011, 10, 31))
        u4 = Sass(username='Hello1234', question1='Answer is 12345', question2='ahhhh', question3='please', question4='Finally a question I know',doquestion=date(2023, 4, 18))

        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.username}")
            