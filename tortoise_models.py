from tortoise import fields
from tortoise.models import Model
from enum import Enum, unique
from datetime import datetime
import pytz
class Pillar(Model):
    name = fields.CharField(max_length=10)
    description = fields.TextField(blank=True, null=True)
    color = fields.CharField(max_length=10, default='#000000')
class ActivityRewards(Model):
    done_reward = fields.IntField()
    reward_treshold_minutes = fields.IntField()
    reward_total_treshold = fields.IntField()
    reward_per_minute = fields.IntField()
    reward_after_treshold = fields.IntField()
    reward_while_cam_on = fields.IntField()
class Activity(Model):
    name = fields.CharField(max_length=100)
    pillar: fields.ForeignKeyRelation[Pillar] | None = fields.ForeignKeyField( model_name="models.Pillar", on_delete=fields.SET_NULL, null=True)
    description = fields.TextField(blank=True, null=True)
    activity_rewards: fields.ForeignKeyRelation[ActivityRewards] = fields.OneToOneField( model_name="models.ActivityRewards", on_delete=fields.RESTRICT)

def get_current_time_in_tz():
    # tz = pytz.timezone('Etc/GMT-2')
    return datetime.now()



class Role(Model):
    name = fields.CharField(max_length=30)
    description = fields.TextField(blank=True, null=True)
    color = fields.CharField(max_length=10, default='#000000')
    prestige = fields.IntField(default=0)


class RolePillar(Model):
    pillar = fields.ForeignKeyField(model_name='models.Pillar', on_delete=fields.CASCADE)
    role = fields.ForeignKeyField(model_name='models.Role', on_delete=fields.CASCADE)
    level = fields.IntField(default=0)


# class RoleLevel(Model):
#     role: fields.ForeignKeyRelation[Role] = fields.ForeignKeyField(
#         model_name='models.Role')
#     pillar: fields.ForeignKeyRelation[Pillar] = fields.ForeignKeyField(
#         model_name='models.Pillar')


class User(Model):
    discord_id = fields.CharField(max_length=100, blank=True, null=True)
    display_name = fields.CharField(max_length=30, null=True)
    timezone = fields.IntField(blank=True, default=2)
    role: fields.ForeignKeyRelation[Role] = fields.ForeignKeyField(
        model_name="models.Role", default=1)
    # object = UserManager()


class Server(Model):
    id = fields.CharField(max_length=100, pk=True)
    name = fields.CharField(max_length=100)
    # admins = fields.ManyToManyField(
    #     model_name="models.User", related_name='admin_servers')


class Session(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE)
    server: fields.ForeignKeyRelation[Server] | None = fields.ForeignKeyField(
        model_name="models.Server", on_delete=fields.SET_NULL, blank=True, null=True)
    activity: fields.ForeignKeyRelation[Activity] = fields.ForeignKeyField(model_name="models.Activity", on_delete=fields.CASCADE)
    joined_at = fields.DatetimeField(default=datetime.now())
    left_at = fields.DatetimeField(null=True)
    duration_in_seconds = fields.IntField(default=0)
    is_active = fields.BooleanField(default=True)


class PlannedEnum(Enum):
    TODAY = 'TODAY'
    THIS_WEEK = 'THIS_WEEK'
    THIS_MONTH = 'THIS_MONTH'
    NEXT_MONTH = 'NEXT_MONTH'


class PriorityEnum(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY HIGH'


class ActivityRecordType(Enum):
    VC = 'VC'
    SS = 'SS'
    BOTH = 'BOTH'
    CAM = 'CAM'
    NONE = 'NONE'
    LOG = 'LOG'


class SessionData(Model):
    session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField(
        model_name="models.Session", on_delete=fields.CASCADE)

    activity_record_type = fields.CharEnumField(
        ActivityRecordType,
        max_length=50,
    )
    duration_in_seconds = fields.IntField(default=0)
    partials_amount = fields.IntField(default=0)


class SessionPartial(Model):
    session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField(
        model_name="models.Session", on_delete=fields.CASCADE)
    joined_at = fields.DatetimeField(default=datetime.now())
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(model_name="models.User", on_delete=fields.CASCADE)
    left_at = fields.DatetimeField(null=True)
    activity_record_type = fields.CharEnumField(
        ActivityRecordType,
        max_length=50,
    )


class Project(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField(blank=True, null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE)
    start_date = fields.DatetimeField(
        blank=True, null=True
    )
    end_date = fields.DatetimeField(
        blank=True, null=True
    )
    priority = fields.CharEnumField(PriorityEnum,
                                    blank=True, null=True)


class Task(Model):
    name = fields.CharField(max_length=255)
    completed = fields.BooleanField(default=False)
    add_date = fields.DatetimeField(default=datetime.now())
    due_date = fields.DatetimeField(
        blank=True, null=True)

    planned = fields.CharEnumField(
        PlannedEnum,
    )
    priority = fields.CharEnumField(PriorityEnum,
                                    max_length=50, blank=True, null=True)
    project: fields.ForeignKeyRelation[Project] | None = fields.ForeignKeyField(
        model_name="models.Project", on_delete=fields.CASCADE, blank=True, null=True)

    session: fields.ForeignKeyRelation[Session] | None = fields.ForeignKeyField(
        model_name="models.Session", on_delete=fields.SET_NULL, blank=True, null=True)


class Tag(Model):
    name = fields.CharField(max_length=255)


class TaskTag(Model):
    task: fields.ForeignKeyRelation[Task] = fields.ForeignKeyField(
        model_name="models.Task", on_delete=fields.CASCADE)
    tag: fields.ForeignKeyRelation[Tag] = fields.ForeignKeyField(
        model_name="models.Tag", on_delete=fields.CASCADE)


class UserPillar(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE)
    pillar: fields.ForeignKeyRelation[Pillar] = fields.ForeignKeyField(
        model_name="models.Pillar", on_delete=fields.CASCADE)
    xp = fields.IntField(default=0)
    level = fields.IntField(default=0)


# class ActivityHabit(Model):
#     name = fields.CharField(max_length=100)
#     min_time = fields.IntField()
#     suggested_weekly_times = fields.IntField()
#     suggested_level = fields.IntField()






class TextChannelEnum(Enum):
    LEADERBOARD = 'Leaderboard'
    TASKS = 'Tasks'
    VOICE = 'Voice'
    TEXT = 'Text'
    CATEGORY = 'Category'


class Channel(Model):
    server: fields.ForeignKeyRelation[Server] = fields.ForeignKeyField(
        model_name="models.Server", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=100)
    channel_type: TextChannelEnum = fields.CharEnumField(
        TextChannelEnum,
        max_length=50
    )
    discord_id = fields.CharField(max_length=100)
    activity: fields.ForeignKeyRelation[Activity] | None = fields.ForeignKeyField(
        model_name="models.Activity", on_delete=fields.SET_NULL, default=None, null=True)


# class UserHabits(Model):
#     user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
#         model_name="models.User", on_delete=fields.CASCADE)
#     activity_habit: fields.ForeignKeyRelation[ActivityHabit] = fields.ForeignKeyField(
#         model_name="models.ActivityHabit", on_delete=fields.CASCADE)
#     start_date = fields.DatetimeField()
#     stopped_date = fields.DatetimeField()
#     frequency = fields.IntField()
#     completed = fields.BooleanField()


class UserServer(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name='models.User', on_delete=fields.CASCADE)
    server: fields.ForeignKeyRelation[Server] = fields.ForeignKeyField(
        model_name='models.Server', on_delete=fields.CASCADE)
    joined_at = fields.DatetimeField(default=datetime.now())
