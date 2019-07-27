from flask_mongoengine import BaseQuerySet
import mongoengine as me


class Movie(me.Document):
    meta = {
        "collection": "movies",
        "queryset_class": BaseQuerySet
    }

    title = me.StringField(min_length=1, max_length=128, required=True)
    release_date = me.DateTimeField()
    actors = me.ListField(me.StringField(max_length=64, required=True))
    genres = me.ListField(me.StringField(max_length=32, required=True))
    sum_of_marks = me.IntField(default=0, min_value=0, required=True)
    number_of_marks = me.IntField(default=0, min_value=0, required=True)
