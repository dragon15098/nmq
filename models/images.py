from mongoengine import *

class Image(Document):
    src = StringField()
    title = StringField()
    description = StringField()
    image = FileField()
