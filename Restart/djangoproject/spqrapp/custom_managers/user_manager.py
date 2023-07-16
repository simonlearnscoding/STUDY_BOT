from django.db import models
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
class UserManager(models.Manager):

    async def get_or_create_user(self, member):
        data = {
            "id": member.id,
            "name": member.name,
            "nick": member.nick
        }
        all_users = await self.get_all()
        try:
            user = await sync_to_async(self.get, thread_sensitive=True)(**data)
        except self.model.DoesNotExist:
            try:
                user = await sync_to_async(self.create, thread_sensitive=True)(**data)
            except Exception as e:
                print(e)
        except self.model.MultipleObjectsReturned:
            users = await sync_to_async(self.filter, thread_sensitive=True)(**data)
            user = users[0]
            for extra_user in users[1:]:
                await sync_to_async(extra_user.delete, thread_sensitive=True)()
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
        try:
            user = self.get(id=int(member.id))
            user.filter = filter
            await sync_to_async(user.save)()
        except Exception as e:
            print(e)