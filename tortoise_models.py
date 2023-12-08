from tortoise import fields
from tortoise.models import Model
from enum import Enum
from datetime import datetime
import pytz
# from django.utils import timezone

# Create a timezone object for GMT+2


def get_current_time_in_tz():
    tz = pytz.timezone('Etc/GMT-2')
    return datetime.now(tz)


class Role(Model):
    name = fields.CharField(max_length=30)
    level_to_reach_it = fields.IntField(default=999)
    description = fields.TextField(blank=True, null=True)
    color = fields.CharField(max_length=10, default='#000000')


class User(Model):
    discord_id = fields.CharField(max_length=100, blank=True, null=True)
    display_name = fields.CharField(max_length=30, null=True)
    timezone = fields.IntField(blank=True, null=True, default=2)
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

    joined_at = fields.DatetimeField(default=get_current_time_in_tz)
    # object = SessionManager()


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
    CAM = 'CAM'
    SS = 'SS'
    BOTH = 'BOTH'
    VOICE = 'VOICE'
    NONE = 'NONE'
    LOG = 'LOG'


class SessionData(Model):
    session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField(
        model_name="models.Session", on_delete=fields.CASCADE)

    activity_record_type = fields.CharEnumField(
        ActivityRecordType,
        max_length=50,
    )
    total_record_seconds = fields.IntField()
    percentage_of_total = fields.IntField()


class SessionPartial(Model):
    session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField(
        model_name="models.Session", on_delete=fields.CASCADE)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    is_active = fields.BooleanField()
    total_record_seconds = fields.IntField()
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
    add_date = fields.DatetimeField(default=get_current_time_in_tz)
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


class Pillar(Model):
    name = fields.CharField(max_length=10)
    description = fields.TextField(blank=True, null=True)
    color = fields.CharField(max_length=10, default='#000000')


class UserPillar(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE)
    pillar: fields.ForeignKeyRelation[Pillar] = fields.ForeignKeyField(
        model_name="models.Pillar", on_delete=fields.CASCADE)
    xp = fields.IntField(default=0)
    level = fields.IntField(default=0)


class ActivityHabit(Model):
    name = fields.CharField(max_length=100)
    min_time = fields.IntField()
    suggested_weekly_times = fields.IntField()
    suggested_level = fields.IntField()


class ActivityRewards(Model):
    name = fields.CharField(max_length=100)
    done_reward = fields.IntField()
    habit_win_reward = fields.IntField()
    streak_reward = fields.IntField()
    reward_treshold = fields.IntField()
    reward_per_minute = fields.IntField()
    reward_after_treshold = fields.IntField()


class Activity(Model):
    name = fields.CharField(max_length=100)
    pillar: fields.ForeignKeyRelation[Pillar] | None = fields.ForeignKeyField(
        model_name="models.Pillar", on_delete=fields.SET_NULL, null=True)
    description = fields.TextField(blank=True, null=True)
    activity_habit: fields.ForeignKeyRelation[ActivityHabit] = fields.OneToOneField(
        model_name="models.ActivityHabit", on_delete=fields.RESTRICT)
    creation_date = fields.DatetimeField(default=get_current_time_in_tz)
    activity_rewards: fields.ForeignKeyRelation[ActivityRewards] = fields.OneToOneField(
        model_name="models.ActivityRewards", on_delete=fields.RESTRICT)


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


class UserHabits(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE)
    activity_habit: fields.ForeignKeyRelation[ActivityHabit] = fields.ForeignKeyField(
        model_name="models.ActivityHabit", on_delete=fields.CASCADE)
    start_date = fields.DatetimeField()
    stopped_date = fields.DatetimeField()
    frequency = fields.IntField()
    completed = fields.BooleanField()


class UserServer(Model):
    user: fields.ForeignKeyRelation[User] = fields.OneToOneField(
        model_name='models.User', on_delete=fields.CASCADE)
    server: fields.ForeignKeyRelation[Server] = fields.OneToOneField(
        model_name='models.Server', on_delete=fields.CASCADE)
    joined_at = fields.DatetimeField(default=get_current_time_in_tz)


class UserLevel(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name="models.User", on_delete=fields.CASCADE, related_name='user_levels')
    pillar: fields.ForeignKeyRelation[Pillar] = fields.ForeignKeyField(
        model_name="models.Pillar", on_delete=fields.CASCADE)
    level = fields.IntField(default=1)
    xp = fields.IntField(default=0)
