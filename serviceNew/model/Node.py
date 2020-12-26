from mongoengine import *


class Node(Document):
    root = BooleanField(default=False)
    parent = ObjectIdField()
    children = ListField(ObjectIdField(), default=[])
    move = StringField(default="")
    color = StringField(default="")
    games = ListField(ObjectIdField(), default=[])
    yearPickCount = DictField()
