from spqrapp.models import User, Session

users = User.objects.all()
print(users)