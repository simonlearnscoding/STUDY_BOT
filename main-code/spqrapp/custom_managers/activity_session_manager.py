from datetime import datetime
from django.apps import apps
from django.db import models
from asgiref.sync import sync_to_async
import modules.session_tracking.activities as act
import pytz
gmt2 = pytz.timezone('Etc/GMT-2')
class BaseLogManager(models.Manager):

    async def get_member_ongoing_log(self, user):
        try:
            # ongoing_log = await sync_to_async(list)(self.filter, thread_sensitive=True)(user=user, status="ONGOING")
            # print(ongoing_log)
            # return await sync_to_async(ongoing_log.first, thread_sensitive=True)()
            # You need to pass a callable object to sync_to_async.
            filter_fn = sync_to_async(self.filter)
            # Now you can call the resulting coroutine with the required arguments.
            ongoing_log = await filter_fn(user=user, status="ONGOING")
            # If you want to convert the result to a list, you can do it like this.
            ongoing_log_list = await sync_to_async(list)(ongoing_log)
            # TODO: I have to figure out what to do if there's more than one member ongoing log
            print(ongoing_log_list)
            return ongoing_log[0]
        except Exception as e:
            print(e)
            return None

    async def get_all_filtered(self, filter):
        try:
            return await sync_to_async(list)(self.filter(filter))
        except Exception as e:
            print(e)

    async def get_all_completed_filtered(self):
        try:
            return await sync_to_async(list)(self.filter(status="COMPLETED"))
        except Exception as e:
            print(e)
            return None

    async def complete_all(self):
        try:
            logs = self.filter(status="ONGOING")
            for log in logs:
                log.status = "COMPLETED"
                log.left_at = datetime.now(gmt2)
                log.duration = (log.left_at - log.joined_at).total_seconds()
                await sync_to_async(log.save)()
            return logs
        except Exception as e:
            print(e)
            return None
    async def complete_log(self, user):
        try:
            log = await self.get_member_ongoing_log(user)
            if log:
                log.status = "COMPLETED"
                log.left_at = datetime.now(gmt2)
                log.duration = (log.left_at - log.joined_at).total_seconds()
                await sync_to_async(log.save, thread_sensitive=True)()
                return log
            else:
                return None
        except Exception as e:
            print(e)
            return None
    async def delete_all(self):
        try:
            logs = self.all()
            await sync_to_async(logs.delete)()
            print("All logs deleted.")
        except Exception as e:
            print(e)

class ActivityLogManager(BaseLogManager):

    async def get_activity_type(self, state):
        activity_type_name = act.getActivityType(state)
        ActivityType = apps.get_model('spqrapp', 'ActivityType')
        activity_type, created = await sync_to_async(ActivityType.objects.get_or_create, thread_sensitive=True)(name=activity_type_name)
        return activity_type

    async def create_activity_log(self, member, after, session):
        data = {
            "session": session,
           "activity_type": await self.get_activity_type(after),
            "activity": act.getActivity(after.channel.id),
            "joined_at": datetime.now(gmt2),
            "user": member,
            "nick": member.nick,
        }
        try:
            log = await sync_to_async(self.create)(**data)
            return log
        except Exception as e:
            print(e)
            return None

class SessionManager(BaseLogManager):
    async def create_session_log(self, member, after):
        data = {
            "activity": act.getActivity(after.channel.id),
            "joined_at": datetime.now(gmt2),
            "user": member,
            "nick": member.nick,
        }
        try:
            return await sync_to_async(self.create)(**data)
        except Exception as e:
            print(e)
            return None

from django.core.exceptions import ObjectDoesNotExist
