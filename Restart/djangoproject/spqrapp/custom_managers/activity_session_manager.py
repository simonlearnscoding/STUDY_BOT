from datetime import datetime
from django.db import models
from asgiref.sync import sync_to_async
import modules.session_tracking.activities as act
import pytz
gmt2 = pytz.timezone('Etc/GMT-2')
class BaseLogManager(models.Manager):

    async def get_member_ongoing_log(self, user):
        try:
            return await sync_to_async(self.filter)(user=user, status="ONGOING").first()
        except Exception as e:
            print(e)
            return None

    async def get_all_ongoing(self):
        try:
            return await sync_to_async(list)(self.filter(status="ONGOING"))
        except Exception as e:
            print(e)
            return None

    async def get_all_completed(self):
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
                log.left_at = datetime.now()
                log.duration = (log.left_at - log.joined_at).total_seconds()
                await sync_to_async(log.save)()
            return logs
        except Exception as e:
            print(e)
            return None
    async def complete_log(self, user):
        try:
            log = self.get_member_ongoing_log(user)
            if log:
                log.status = "COMPLETED"
                log.left_at = datetime.now(gmt2)
                log.duration = (log.left_at - log.joined_at).total_seconds()
                await sync_to_async(log.save)()
                return log
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
    async def create_activity_log(self, member, after, session):
        data = {
            "session": session,
            "activity_type": act.getActivityType(after),
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
