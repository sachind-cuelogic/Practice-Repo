from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from accounts_app import views

urlpatterns = [

    url(r'^industries/$',
        views.IndustryList.as_view(), name='industries_create'),
    url(r'^industries/(?P<id>[0-9]+)/$',
        views.IndustryDetails.as_view(),
        name='industries_update_list'),

    url(r'^accounts/$',
        views.AccountList.as_view(), name='account_create_list'),

    url(r'^accounts/(?P<id>[0-9]+)/$',
        views.AccountDetails.as_view(),
        name='account_update_list'),

    url(r'^category/$',
        views.ListCreateCategoryView.as_view(), name='category_create_list'),

    url(r'^category/(?P<id>[0-9]+)/$',
        views.UpdateDestroySearchCategoryView.as_view(),
        name='category_update_list'),

    url(r'^products/$',
        views.ProductList.as_view(), name='product_list'),

    url(r'^products/(?P<id>[0-9]+)/$',
        views.ProductDetails.as_view(),
        name='product_details'),

    url(r'^plans/$',
        views.PlansList.as_view(), name='plan_list'),

    url(r'^plans/(?P<id>[0-9]+)/$',
        views.PlansDetails.as_view(),
        name='plan_details'),
    
    # url(r'^flagged/products/$',
    #     views.ListFlaggedProductView.as_view(), name='flagged_products'),

    # url(r'^product/support/rating/$',
    #     views.ProductSupportRatingView.as_view(),
    #     name='product_support_rating'),

    # url(r'^product/influencers/(?P<id>[0-9]+)/$',
    #     views.ProductTopInfluencerView.as_view(),
    #     name='product_influencers'),

    url(r'^feature/list/$',
        views.FeatureListView.as_view(), name='feature_list_view'),

    url(r'^bu/unit/$',
        views.BuUnitView.as_view(),
        name='bu_unit_view'),

    url(r'^bu/unit/(?P<id>[0-9]+)/$',
        views.BuUnitRetriveDestroyView.as_view(),
        name='bu_unit_destroy'),

    url(r'^functional/group/(?P<id>[0-9]+)/$',
        views.FunctionalGroupRetriveDestroyAPIView.as_view(),
        name='functional_group_destroy'),

    url(r'^functional/group/$',
        views.FunctionalGroupAPIView.as_view(),
        name='functional_group_view'),

    url(r'^crm/info/$',
        views.CrmInfoAPIView.as_view(),
        name='crm_info_view'),

    url(r'^crm/details/(?P<id>[0-9]+)/$',
        views.CrmDetailView.as_view(),
        name='crm_details'),
    
    url(r'^account/detail/(?P<id>[0-9]+)/$',
        views.AccountDetailView.as_view(),
        name='account_detail'),

    url(r'^buUnit/details/(?P<id>[0-9]+)/$',
        views.BuUnitDetailView.as_view(),
        name='bu_unit_detail'),

    # url(r'^admin/user/details/(?P<id>[0-9]+)/$',
    #     views.AdminUserDetailView.as_view(),
    #     name='admin_user_detail'),

    # url(r'^admin/accounts/filter/$',
    #     views.AdminAccountFilter.as_view(), name='admin_account_filter'),


    # url(r'^functional/group/details/(?P<id>[0-9]+)/$',
    #     views.FunctinalGroupDetailView.as_view(),
    #     name='functional_details'),

    url(r'^BU/enable/data/$',
        views.BuUnitGoButtonView.as_view(),
        name='enable_disable_view'),

    url(r'^account/enable/data/$',
        views.AccountGoButtonView.as_view(),
        name='enable_disable_view'),

    # url(r'^user/enable/data/$',
    #     views.UserGoButtonView.as_view(),
    #     name='enable_disable_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
