from django.db import models
from enum import Enum

class AssetsManagement(models.Model):
    """
    Base class to stores attachments
    """

    class AssetTypes(Enum):
        IMAGE = 1
        AUDIO = 2
        VIDEO = 3

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    name = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='assets', blank=True,
                                  null=True)
    cover_photo = models.ImageField(upload_to='assets', blank=True,
                                    null=True)
    cover_photo_name = models.TextField(null=True, blank=True)
    asset_type = models.CharField(blank=True, null=True, max_length=20,
                                  choices=AssetTypes.as_tuple())
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'assets_management'


