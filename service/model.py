from mongoengine import *

import datetime


class Gibo(Document):
    giboName = StringField(required=True, max_length=200)
    giboDate = StringField(required=True)
    giboLocation = StringField(required=True, max_length=50)
    giboMinutes = StringField(required=True)
    giboSeconds = StringField(required=True)
    giboTimeCount = StringField(required=True)
    giboKomi = StringField(required=True)
    giboResult = StringField(required=True)
    giboBlackPlayerName = StringField(required=True)
    giboBlackPlayerRank = StringField(required=True)
    giboWhitePlayerName = StringField(required=True)
    giboWhitePlayerRank = StringField(required=True)
    giboMoves = ListField(required=True)
    giboLink = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)
    analyzed = BooleanField(default=False)


class Node(Document):
    root = BooleanField(default=False)
    parentID = ObjectIdField()
    childrenID = ListField(ObjectIdField(), default=[])
    move = StringField(default="")
    color = StringField(default="")
    games = ListField(ObjectIdField(), default=[])
    yearPickCount = DictField()
