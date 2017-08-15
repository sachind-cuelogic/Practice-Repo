from attachments.models import AssetsManagement
from attachments.non_null_serializer import BaseSerializer


class AssetsManagementSerializer(BaseSerializer):
    class Meta:
        model = AssetsManagement
