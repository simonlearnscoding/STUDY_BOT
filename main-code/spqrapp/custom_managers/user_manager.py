from django.db import models
from django.apps import apps
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist


class UserManager(models.Manager):

    async def get_user_filter(self, data):
        #TODO: Test this too
        default = "today-study-exclude_no_cam"
        user = await self.get_or_create_user(data["member"])
        if user.filter is None:
            return default
        else:
            return user.filter
    def remove_emojis(self, data):
        if not data:
            return data
        if not isinstance(data, str):
            return data
        return ''.join(c for c in data if c <= '\uFFFF')
    async def get_or_create_user(self, member):
        User = apps.get_model('spqrapp', 'User')
        data = {
            "id": member.id,
            "name": self.remove_emojis(member.name),
            "nick": self.remove_emojis(member.nick) if member.nick else self.remove_emojis(member.name)
        }
        try:
            user, created = await sync_to_async(User.object.get_or_create, thread_sensitive=True)(**data)
        except Exception as e:
            print(e)
        return user


    async def delete_all(self):
        try:
            await sync_to_async(self.all().delete)()
        except Exception as e:
            print(e)



    async def get_all(self):
        try:
            all = await sync_to_async(self.all)()
            return list(all[:5])
        except Exception as e:
            print(e)

    async def change_user_filter(self, member, filter):
        #TODO: Test
        try:
            user = await self.get_or_create_user(member)
            user.filter = filter
            await sync_to_async(user.save)() #TODO: I might have to change it here too then
        except Exception as e:
            print(e)
