from enum import Enum
from spqrapp.custom_managers.activity_session_manager import ActivityLogManager, SessionManager
from spqrapp.custom_managers.user_manager import UserManager
from django.utils import timezone
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255)
    min_level = models.IntegerField()
    pillar = models.ForeignKey('Pillar', on_delete=models.CASCADE)


class RoleName(models.TextChoices):
    INERTUS = 'INERTUS'
    GLADIATOR = 'GLADIATOR'
    LEGIONARY = 'LEGIONARY'
    PHILOSOPHER = 'PHILOSOPHER'
    SENATOR = 'SENATOR'
    CENTURION = 'CENTURION'
    ATHENAEUM = 'ATHENAEUM'
    IMPERATOR = 'IMPERATOR'

class Role(models.Model):
    name = models.CharField(max_length=30)
    level_to_reach_it = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=10)


class User(models.Model):
    discord_id = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=30, null=True)
    timezone = models.IntegerField(blank=True, null=True, default=2)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    object = UserManager()


class Session(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    server = models.ForeignKey(
        'Server', on_delete=models.SET_NULL, blank=True, null=True)

    joined_at = models.DateTimeField(default=timezone.now)
    object = SessionManager()


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class PlannedEnum(BaseEnum):
    TODAY = 'TODAY'
    THIS_WEEK = 'THIS_WEEK'
    THIS_MONTH = 'THIS_MONTH'
    NEXT_MONTH = 'NEXT_MONTH'


class PriorityEnum(BaseEnum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY HIGH'


class ActivityRecordType(BaseEnum):
    CAM = 'CAM'
    SS = 'SS'
    BOTH = 'BOTH'
    VOICE = 'VOICE'
    NONE = 'NONE'
    LOG = 'LOG'


class SessionData(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    activity_record_type = models.CharField(
        max_length=50,
        choices=ActivityRecordType.choices()
    )
    total_record_seconds = models.IntegerField()
    percentage_of_total = models.IntegerField()


class SessionPartial(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField()
    total_record_seconds = models.IntegerField()
    activity_record_type = models.CharField(
        max_length=50,
        choices=ActivityRecordType.choices()
    )


class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    add_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(
        blank=True, null=True)

    planned = models.CharField(
        max_length=50,  # Adjust the max_length as needed
        choices=PlannedEnum.choices(),
    )
    priority = models.CharField(
        max_length=50, blank=True, null=True, choices=PriorityEnum.choices())
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, blank=True, null=True)

    session = models.ForeignKey(
        'Session', on_delete=models.SET_NULL, blank=True, null=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    start_date = models.DateTimeField(
        blank=True, null=True
    )
    end_date = models.DateTimeField(
        blank=True, null=True
    )
    priority = models.CharField(
        max_length=50, blank=True, null=True, choices=PriorityEnum.choices())


class TaskTag(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class UserPillar(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    pillar = models.ForeignKey('Pillar', on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)


class Pillar(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=10)


class Server(models.Model):
    discord_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    admin = models.ForeignKey('User', null=True, related_name='admin_servers', on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.admins.exists():
            raise ValueError("A server must have at least one admin")


class Channel(models.Model):
    server = models.ForeignKey('Server', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    discord_id = models.CharField(max_length=100)
    activity = models.ForeignKey(
        'Activity', on_delete=models.SET_NULL, null=True)


class Activity(models.Model):
    name = models.CharField(max_length=100)
    pillar = models.ForeignKey('Pillar', on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    activity_habit = models.OneToOneField(
        'ActivityHabit', on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    activity_rewards = models.OneToOneField(
        'ActivityRewards', on_delete=models.SET_NULL, null=True)


class ActivityRewards(models.Model):
    name = models.CharField(max_length=100)
    done_reward = models.IntegerField()
    habit_win_reward = models.IntegerField()
    streak_reward = models.IntegerField()
    reward_treshold = models.IntegerField()
    reward_per_minute = models.IntegerField()
    reward_after_treshold = models.IntegerField()


class ActivityHabit(models.Model):
    name = models.CharField(max_length=100)
    min_time = models.IntegerField()
    suggested_weekly_times = models.IntegerField()
    suggested_level = models.IntegerField()


class UserHabits(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    activity_habit = models.ForeignKey(
        'ActivityHabit', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    stopped_date = models.DateTimeField()
    frequency = models.IntegerField()
    completed = models.BooleanField()


class UserServer(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    server = models.OneToOneField('Server', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)


class UserLevel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_levels')
    pillar = models.ForeignKey('Pillar', on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)


# Create your models here.


# class ActivityType(models.Model):
#     name = models.CharField(max_length=255)
#     pillar = models.CharField(max_length=255, choices=Pillar.choices)


# class Switches(models.Model):
#     name = models.CharField(max_length=255)
#     switch = models.DateTimeField(blank=True, null=True)
#

# class VCType(models.Model):
#     name = models.CharField(max_length=255)


# class Session(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='sessions')
#     joined_at = models.DateTimeField(default=timezone.now)
#     activity = models.CharField(max_length=255)
#     left_at = models.DateTimeField(blank=True, null=True)
#     nick = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(
#         max_length=255, choices=SessionStatus.choices, default=SessionStatus.ONGOING)
#     duration = models.IntegerField(default=0)
#     object = SessionManager()


# class ActivityLog(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='activity_logs')
#     session = models.ForeignKey(
#         Session, on_delete=models.CASCADE, related_name='activity_logs')
#     nick = models.CharField(max_length=255, blank=True, null=True)
#     activity = models.CharField(max_length=255)
#     activity_type = models.CharField(max_length=255)
#     joined_at = models.DateTimeField(default=timezone.now)
#     left_at = models.DateTimeField(blank=True, null=True)
#     duration = models.IntegerField(blank=True, null=True, default=0)
#     xp = models.IntegerField(blank=True, null=True)
#     status = models.CharField(
#         max_length=255, choices=SessionStatus.choices, default=SessionStatus.ONGOING)
#     activity_type = models.ForeignKey(
#         ActivityType, on_delete=models.SET_NULL, blank=True, null=True)
#     vc_type = models.ForeignKey(
#         VCType, on_delete=models.SET_NULL, blank=True, null=True)
#     object = ActivityLogManager()

# class SessionStatus(models.TextChoices):
#     ONGOING = 'ONGOING'
#     COMPLETED = 'COMPLETED'


# class Pillar(models.TextChoices):
    # THINKER = 'THINKER'
    # DISCIPLINE = 'DISCIPLINE'
    # PHYSICAL_WORK = 'PHYSICAL_WORK'
