from accounts_app.non_null_serializer import BaseSerializer
from accounts_app.models import (
    Account,
    Category,
    Industries,
    Product,
    Plans,
    FunctionalGroup,
    BuUnit,
    CrmInfo
)

class IndustriesSerializer(BaseSerializer):
    class Meta:
        model = Industries
        fields = ('id', 'name', 'is_active',
                 'created_by', 'updated_by')
        read_only_fields = ('id')


class AccountSerializer(BaseSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'email', 'website',
                 'is_active', 'is_registered', 'plans',
                 'industries', 'updated_by', 'code',
                 'plan_start_date','created_by', 'is_enable')

        read_only_fields = ('id',)


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'organization', 'is_active',
                  'created_by', 'updated_by')
        read_only_fields = ('id',)


class ProductSerializer(BaseSerializer):
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'organization', 'is_active',
                  'created_by', 'updated_by', 'attachments', 'description')
        read_only_fields = ('id',)


class PlansSerializer(BaseSerializer):
    class Meta:
        model = Plans
        fields = ('id', 'plan_type', 'price', 'duration', 'created_at',
                  'created_by', 'is_active', 'updated_by')
        read_only_fields = ('id', 'created_at',)


class FunctionalGroupSerializer(BaseSerializer):
    class Meta:
        model = FunctionalGroup
        exclude = ('updated_date',)


class BuUnitSerializer(BaseSerializer):
    functional_group = FunctionalGroupSerializer(many=True)
    class Meta:
        model = BuUnit


class BuUnitCreateSerializer(BaseSerializer):
    class Meta:
        fields = ('id', 'name', 'email', 'website',
         'is_active','plans','account', 'code',
         'plan_start_date','created_by', 'is_enable',)
        model = BuUnit


class CrmInfoSerializer(BaseSerializer):
    class Meta:
        model = CrmInfo
