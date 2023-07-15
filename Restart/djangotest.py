import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoproject.myproject.settings'

import django
django.setup()
from djangoproject.spqrapp.models import User, Session
users = User.objects.all()
print(users)

from django.db import transaction


def create_query(self, filter):
    print(filter)
def create_object(model, data):
    try:
        obj = model.objects.create(**data)
        print(f"Created {model.__name__} object: {obj}")
        return obj
    except Exception as e:
        print(e)

def create_user(member):
    data = {
        "id": member.id,
        "name": member.name,
    }
    create_object(User, data)
class Member:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Now you can create a Member object and pass it to create_user
member = Member(12224, 'sepp')
create_user(member)
