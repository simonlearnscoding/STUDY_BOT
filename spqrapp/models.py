
from spqrapp.custom_managers.activity_session_manager import ActivityLogManager, SessionManager
from spqrapp.custom_managers.user_manager import UserManager
from django.utils import timezone
from django.db import models
import os

print(os.getcwd())


class SessionStatus(models.TextChoices):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'


class Pillar(models.TextChoices):
    THINKER = 'THINKER'
    DISCIPLINE = 'DISCIPLINE'
    PHYSICAL_WORK = 'PHYSICAL_WORK'


class User(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, default="no nick")
    filter = models.CharField(max_length=255, blank=True, null=True)
    object = UserManager()


class ActivityType(models.Model):
    name = models.CharField(max_length=255)
    pillar = models.CharField(max_length=255, choices=Pillar.choices)


class Switches(models.Model):
    name = models.CharField(max_length=255)
    switch = models.DateTimeField(blank=True, null=True)


class VCType(models.Model):
    name = models.CharField(max_length=255)


class Session(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions')
    joined_at = models.DateTimeField(default=timezone.now)
    activity = models.CharField(max_length=255)
    left_at = models.DateTimeField(blank=True, null=True)
    nick = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=255, choices=SessionStatus.choices, default=SessionStatus.ONGOING)
    duration = models.IntegerField(default=0)
    object = SessionManager()


class ActivityLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activity_logs')
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='activity_logs')
    nick = models.CharField(max_length=255, blank=True, null=True)
    activity = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)
    joined_at = models.DateTimeField(default=timezone.now)
    left_at = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True, default=0)
    xp = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=255, choices=SessionStatus.choices, default=SessionStatus.ONGOING)
    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.SET_NULL, blank=True, null=True)
    vc_type = models.ForeignKey(
        VCType, on_delete=models.SET_NULL, blank=True, null=True)
    object = ActivityLogManager()


class UserLevel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_levels')
    pillar = models.CharField(max_length=255, choices=Pillar.choices)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)


class Role(models.Model):
    name = models.CharField(max_length=255)
    min_level = models.IntegerField()
    pillar = models.CharField(max_length=255, choices=Pillar.choices)


class RoleName(models.TextChoices):
    INERTUS = 'INERTUS'
    GLADIATOR = 'GLADIATOR'
    LEGIONARY = 'LEGIONARY'
    PHILOSOPHER = 'PHILOSOPHER'
    SENATOR = 'SENATOR'
    CENTURION = 'CENTURION'
    ATHENAEUM = 'ATHENAEUM'
    IMPERATOR = 'IMPERATOR'
# Create your models here.
