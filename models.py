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

class Project(Document):
    id = StringField()
    name = StringField(required=True)
    description = StringField(required=True)

    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField() 


class Task(Document):
    id = StringField()
    name = StringField(required=True)
    description = StringField(required=True)
    status = StringField(required=True, choices = ["Todo","pending","done"])
    assignedTo = ReferenceField(User,reverse_delete_rule=CASCADE)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField() 

