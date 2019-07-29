from bson.objectid import ObjectId
from flask_mongoengine import BaseQuerySet
import mongoengine as me


class Choice(me.EmbeddedDocument):
    id = me.ObjectIdField(default=ObjectId, required=True)
    title = me.StringField(max_length=128, required=True)
    votes = me.IntField(default=0, min_value=0, required=True)


class Voting(me.Document):
    meta = {
        "collection": "votings",
        "queryset_class": BaseQuerySet
    }

    choices = me.EmbeddedDocumentListField(Choice, required=True)
    current_votes = me.IntField(default=0, min_value=0, required=True)
    max_votes = me.IntField(min_value=1)
    start_date = me.DateTimeField()
    finish_date = me.DateTimeField()
