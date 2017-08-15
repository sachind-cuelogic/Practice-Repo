from django.db import models
from enum import Enum
# from django.db.models import CharField
from django_mysql.models import ListCharField

class Agent(models.Model):
    """
    Base Class for storing Agent
    Agent are different user of a company that
    deals with ticket.
    Agents are created only by admin's of the organization.
    Agent's can be supervisor's of different agents.
    """

    class Gender(Enum):
        MALE = 'Male'
        FEMALE = 'Female'
        OTHERS = 'Others'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    address = ListCharField(
                models.IntegerField(),
                size=100,
                max_length=(100*126)
    )

    gender = models.CharField(null=True, max_length=20,
                              choices=Gender.as_tuple())
    birthday = models.DateField(null=True)
    profile_picture = models.ImageField(
            upload_to='agent_picture/',
            null=True,
            blank=True
    )

    is_admin = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    account = models.CharField(max_length=10, null=True, blank=True)
    user = models.CharField(max_length=10, null=True, blank=True)
    category =  ListCharField(
                models.IntegerField(),
                size=100,
                max_length=(100*126)
    )

    assendents = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=10, null=True, blank=True)
    updated_by = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    total_resolved_issues = models.IntegerField(default=0)
    total_open_issue = models.IntegerField(default=0)
    total_resolved_ticket_heat_index = models.IntegerField(default=0)
    average_resolved_ticket_heat_index = models.FloatField(default=0)

    class Meta:
        db_table = 'agent'
