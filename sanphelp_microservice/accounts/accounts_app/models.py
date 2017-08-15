from django.db import models
from django.db.models.signals import (pre_save,
                                      post_save,
                                      post_delete)
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import m2m_changed
from enum import Enum

class Plans(models.Model):
    """
    Base Class capturing all plans information
    that provider can buy.
    """
    plan_type = models.CharField(max_length=50)
    price = models.FloatField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.plan_type

    class Meta:
        db_table = 'plan'


class FunctionalGroup(models.Model):
    """
    Base Model for storing Functional Group
    """

    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'functional_group'


class CrmInfo(models.Model):
    """
    Base Model for storing CrmInfo
    """

    class CRMNAME(Enum):
        SIEBEL = 'siebel'
        SALESFORCE = 'salesforce'
        DYNAMICCRM = 'dynamic_crm'
        SERVICENOW = 'service_now'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    name = models.CharField(max_length=80,
        choices=CRMNAME.as_tuple())
    login_url = models.TextField(blank=True, null=True)
    login_body = models.TextField(blank=True, null=True)
    ticket_generate_url = models.TextField(blank=True, null=True)
    ticket_generate_body = models.TextField(blank=True, null=True)
    attachmet_url = models.TextField(blank=True, null=True)
    attachment_body = models.TextField(blank=True, null=True)
    ticket_update_url = models.TextField(blank=True, null=True)
    ticket_update_body = models.TextField(blank=True, null=True)
    ticket_close_url = models.TextField(blank=True, null=True)
    ticket_close_body = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_enable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'crm_information'

class Industries(models.Model):
    """
    Base Class for storing list of industries
    These industries are shown as preferred industries to user
    during boarding time.
    """
    name = models.CharField(max_length=50)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'industries'


class Account(models.Model):
    """
    Base class for storing customer related information
    Customers are basically clients that purchase plans from audetemi
    Every customer will have one user account
    One admin who is goint to add agent system
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=70)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    plans = models.ForeignKey(Plans, null=True, blank=True)
    plan_start_date = models.DateTimeField(auto_now_add=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)
    industries = models.ManyToManyField(Industries, blank=True)
    crm_info = models.ManyToManyField(CrmInfo, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    total_reported_issues = models.IntegerField(default=0)
    total_resolved_issues = models.IntegerField(default=0)
    total_resolved_ticket_heat_index = models.IntegerField(default=0)
    average_resolved_ticket_heat_index = models.FloatField(default=0)
    support_rating_days = models.IntegerField(default=0)
    is_enable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'account'        


class BuUnit(models.Model):
    """
    Base class for storing BU Unit related information
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=70)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    plans = models.ForeignKey(Plans, null=True, blank=True)
    plan_start_date = models.DateTimeField(auto_now_add=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)

    industry = models.ManyToManyField(Industries, blank=True)
    account = models.ForeignKey(Account, blank=True)
    functional_group = models.ManyToManyField(FunctionalGroup,
        blank=True)
    parent_bu_unit = models.ForeignKey("self", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    is_enable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'BuUnit'


class Category(models.Model):
    """
    Base class for storing category related information
    Category are basically differenty types of products
    that a company produces.
    """
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Account)
    is_active = models.BooleanField(default=False)

    flag_length = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    expected_number_of_issues = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Product(models.Model):
    """
    Base class for storing Product related information
    Product are basically different items that
    follow under certain category.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    organization = models.ForeignKey(Account)
    is_active = models.BooleanField(default=False)
    attachments = models.ImageField(upload_to='products', blank=True,
                                    null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    total_reported_issues = models.IntegerField(default=0)
    total_resolved_issues = models.IntegerField(default=0)
    total_resolved_ticket_heat_index = models.IntegerField(default=0)
    average_resolved_ticket_heat_index = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'product'

class UsageInformation(models.Model):
    """
    Base Model for storing Usage Information
    """

    bu_unit = models.ForeignKey(BuUnit)
    functional_group = models.ForeignKey(FunctionalGroup)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    """
    To return is_active boolean field 
    """
    # def __unicode__(self):
    #     return self.is_active

    class Meta:
        db_table = 'usage_information'


def functional_group_changed(sender, **kwargs):

    if kwargs.get("action") == "pre_add" and kwargs.get('instance'):
        functiona_ids = kwargs.get('pk_set')

        functional_groups = FunctionalGroup.objects.filter(
            id__in = list(functiona_ids))

        for obj in functional_groups:
            usage_obj = UsageInformation.objects.filter(
                is_active=True,
                functional_group=obj,
                bu_unit=kwargs.get("instance"),
                start_date__isnull=False,
                end_date__isnull=True)

            if not len(usage_obj):
                usage_obj = UsageInformation.objects.create(
                    is_active=True,
                    functional_group=obj,
                    bu_unit=kwargs.get("instance"),
                    start_date=timezone.now())

        usage_obj = UsageInformation.objects.filter(
            is_active=True,
            functional_group__in=functional_groups,
            bu_unit=kwargs.get("instance"),
            start_date__isnull=False,
            end_date__isnull=True).values_list('id', flat=True)

        active_usage_obj = UsageInformation.objects.filter(
            is_active=True,
            bu_unit=kwargs.get("instance"),
            start_date__isnull=False,
            end_date__isnull=True).exclude(id__in=usage_obj)

        for obj in active_usage_obj:
            obj.end_date = timezone.now()
            obj.save()

m2m_changed.connect(functional_group_changed, sender=BuUnit.functional_group.through)
