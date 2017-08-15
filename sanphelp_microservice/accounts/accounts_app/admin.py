from django.contrib import admin

from accounts_app.models import (
    Industries,
    Account,
    Category,
    Product,
    Plans,
    UsageInformation,
    FunctionalGroup,
    CrmInfo,
    BuUnit
)

admin.site.register(Industries)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Plans)
admin.site.register(BuUnit)
admin.site.register(CrmInfo)
admin.site.register(FunctionalGroup)
admin.site.register(UsageInformation)
