from mongoengine import *

class Node(Document):
    root = BooleanField(default=False)
    parent = ReferenceField()
    children = ListField(ReferenceField(), default=[])
    move = StringField(default="")
    color = StringField(default="")
    games = ListField(ReferenceField(), default=[])
    yearPickCount = DictField()
