from mongoengine import *
from uuid import uuid4
from datetime import datetime

class User(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    mobileNumber = StringField(required=True)

    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()