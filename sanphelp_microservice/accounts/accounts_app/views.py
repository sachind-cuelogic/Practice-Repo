from django.shortcuts import render
import base64
from django.core.files.base import ContentFile
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts_app.models import (
    Account,
    Category,
    Industries,
    Product,
    Plans,
    CrmInfo,
    BuUnit,
    FunctionalGroup
)
from accounts_app.serializers import (
    AccountSerializer,
    CategorySerializer,
    IndustriesSerializer,
    ProductSerializer,
    PlansSerializer,
    FunctionalGroupSerializer,
    FunctionalGroup,
    CrmInfoSerializer,
    BuUnitCreateSerializer,
    BuUnitSerializer
)

from accounts_app import helper
from accounts_app.custom_pagination import StandardResultsSetPagination
from accounts_app.system_error import(
	check_for_industry_error,
	check_for_account_error,
	check_for_category_error,
	check_for_product_error,
    check_for_plan_error,
    check_for_functional_group_errors,
    check_for_crm_info_errors,
    check_for_bu_unit_errors
	)
from accounts_app import (
    error_conf
)

###############################################################################
# Defining Base Class For Common Functions
###############################################################################
class BaseListCreateAPI(ListCreateAPIView):
    """
    Base Class to define common Methods
    Used across ListCreateAPIView API
    """
    pagination_class = StandardResultsSetPagination

    def get_kwargs_for_filtering(self):
        """
        This is a self defined method for search.
        It searches on the basic of category name.
        If name is not provided it displays all the categories.

        Note:- the search string should be appended in the urls
        example:- /api/category/?name=Mobiles
        """
        filtering_kwargs = {}
        for field in self.my_filter_fields:
            # iterate over the filter fields
            # get the value of a field from request query parameter
            field_value = self.request.query_params.get(field)
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs



##############################################################################
# Industry CURD API
##############################################################################
class IndustryList(BaseListCreateAPI):
    """
    Method Supported: GET POST

    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to add new industry to system or retrieve existing Industries from system

    Compulsory Fields: name

    Filtering Query Params: name
    """

    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    my_filter_fields = ('name',)

    def get(self, request, format=None):

        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True
        queryset = Industries.objects.filter(**filtering_kwargs)
        serializer = IndustriesSerializer(queryset, many=True)
        return Response({'results': serializer.data})

    def post(self, request, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to add new industry to system.
        """
        error_checks = check_for_industry_error(request)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        industry_data = request.data

        industry_data['is_active'] = True
        serializer = IndustriesSerializer(data=industry_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)	

class IndustryDetails(RetrieveUpdateDestroyAPIView):
    """
    Method Supported: GET PATCH DELETE

    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to retrive, modify or delete existing Industries from system

    Filtering Query Params: id
    """
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    lookup_field = 'id'

    def get(self, request, id, format=None):

        industries_object = get_object_or_404(Industries,
                                              id=id,
                                              is_active=True)
        serializer = IndustriesSerializer(industries_object)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to modify existing Industry from system
        """
        industry_data = request.data
        if industry_data:
            industries_object = get_object_or_404(Industries,
                                                  id=id)
            serializer = IndustriesSerializer(industries_object,
                                              data=industry_data,
                                              partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Data is not provided"},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to delete existing Industry from system
        """
        industries_object = get_object_or_404(Industries,
                                              id=id)

        industries_object.is_active = False
        industries_object.save()
        return Response({'success': True,
                         'msg': 'Industries Deleted Successfully'},
                        status=status.HTTP_200_OK)

##############################################################################
# Accounts CURD API
##############################################################################
class AccountList(BaseListCreateAPI):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to add new Account to system or retrieve existing Account from system

    Compulsory Fields: name, email, industries

    Filtering Query Params: name
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    my_filter_fields = ('name',)

    def get_queryset(self):

        """
        This method is for get list of all accounts.
        It shows only requested user belongs that accounts.
        """

        # user = request.user
        # if user.role == User.UserTypes.NORMAL_USER.value:
        #     acc_id = user.userprofile.bu_unit.account.id
        #     account = Account.objects.filter(id = acc_id)
        # else:
        #     account = Account.objects.filter(is_active = True)

        # accountSerializer = AccountSerializer(account,many=True)
        # return Response(accountSerializer.data,
        #                 status=status.HTTP_200_OK)


        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True
        queryset = Account.objects.filter(**filtering_kwargs)
        return queryset

    def post(self, request, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to add new industry to system.
        """
        error_checks = check_for_account_error(request)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        account_data = request.data
        account_data['is_active'] = True
        account_data['is_enable'] = True
        serializer = AccountSerializer(data=account_data)   

        if serializer.is_valid():
            account = serializer.save()
            data               = {}
            data["is_active"]  = True
            data["is_enable"]  = True
            data["created_by"] = account_data.get("created_by")
            data["name"]       = "Default " + account_data.get("name")
            data["code"]       = "D" + account_data.get("code")
            data["account"]    = account.id
            data["email"]      = account_data.get("email", "")

            if data:
                error_check = check_for_bu_unit_errors(data)

                if (error_check):
                    return Response(error_check,
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            bu_serializer = BuUnitCreateSerializer(data=data)

            if bu_serializer.is_valid():
                bu_serializer.save()            

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class AccountDetails(RetrieveUpdateDestroyAPIView):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to retrive, modify or delete existing Account from system

    Filtering Query Params: id
    """
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    lookup_field = 'id'

    def get(self, request, id, format=None):

        account_object = get_object_or_404(Account,
                                           id=id,
                                           is_active=True)
        serializer = AccountSerializer(account_object)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to modify existing Account from system
        """
        account_data = request.data
        if account_data:
            account_object = get_object_or_404(Account,
                                               id=id)
            serializer = AccountSerializer(account_object,
                                           data=account_data,
                                           partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Data is not provided"},
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        **Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to delete existing account from system
        """
        account_object = get_object_or_404(Account,
                                           id=id)
        account_object.is_active = False
        account_object.save()
        bu_unit = BuUnit.objects.get(account__id=account_object.id)
        bu_unit.is_active = False
        bu_unit.save()

        return Response({'success': True,
                         'msg': 'Account Deleted Successfully'},
                        status=status.HTTP_200_OK)


##########################################################################
# CATEGORY CURD API
##########################################################################
class ListCreateCategoryView(BaseListCreateAPI):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required Admin Login
        API is used to add new Category to system or retrieve existing Categories from system

    Compulsory Fields: name, organization

    Filtering Query Params: name, organization
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    my_filter_fields = ('name',)

    def get_queryset(self):

        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True
        queryset = Category.objects.filter(**filtering_kwargs)
        return queryset

    def post(self, request, format=None):
        """
        This method checks wheather the request is coming
        from the admin of the same account and creates
        category if requested user is the admin of the
        same account.
        """
        error_checks = check_for_category_error(request)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        category_data = request.data
        category_data['is_active'] = True
        serializer = CategorySerializer(data=category_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class UpdateDestroySearchCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required Admin Login
        API is used to retrive, modify or delete existing Category from system

    Filtering Query Params: id
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get(self, request, id, format=None):
        category_object = get_object_or_404(Category,
                                           id=id,
                                           is_active=True)
        serializer = CategorySerializer(category_object)
        return Response(serializer.data)


    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming from the admin of same account.
        It is used to modify existing Category from system
        """

        category_data = request.data
        if category_data:
        	category_object = get_object_or_404(
        		Category, id=id)
        	serializer = CategorySerializer(category_object,
        		data=category_data,
        		partial=True)
        	if serializer.is_valid():
        		serializer.save()
        		return Response(serializer.data,
        			status=status.HTTP_201_CREATED)
    		return Response(serializer.errors,
    			status=status.HTTP_400_BAD_REQUEST)
		return Response({"msg": "Data is not provided"},
			status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        **Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id, format=None):
        """
        This method checks wheather the request is coming
        from the admin of the same account.
         It is used to delete existing Category from system
        """
        category_object = get_object_or_404(
                Category, id=id)
        category_object.is_active = False
        category_object.save()
        return Response({'success': True,
                         'msg': 'Category Deleted Successfully'},
                        status=status.HTTP_200_OK)            

# ##########################################################################
# # PRODUCT CURD API
# ##########################################################################
class ProductList(BaseListCreateAPI):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required Admin Login
        API is used to add new Product to system or retrieve existing Products from system

    Compulsory Fields: name, category, organization

    Filtering Query Params: name, category, organization
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    my_filter_fields = ('name', 'category', 'organization',)

    def get_queryset(self):

        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True
        queryset = Product.objects.filter(**filtering_kwargs)
        return queryset


    def post(self, request, format=None):
        """
        This method checks whether the request is coming from the admin of same account.
        It is used to add new Product to system.
        """
        error_checks = check_for_product_error(request)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        product_data = request.data
        product_data['is_active'] = True

        serializer = ProductSerializer(data=product_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ProductDetails(RetrieveUpdateDestroyAPIView):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required Admin Login
        API is used to retrive, modify or delete existing product from system

    Filtering Query Params: id
    """
    queryset = Category.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get(self, request, id, format=None):
        product_object = get_object_or_404(Product, id=id,
                                           is_active=True)
        serializer = ProductSerializer(product_object)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming from the admin.
        It is used to modify existing Product from system
        """
        product_data = request.data
        if product_data:
        	product_object = get_object_or_404(Product, id=id)

        	serializer = ProductSerializer(product_object,
        		data=product_data,
        		partial=True)

        	if serializer.is_valid():
        		serializer.save()
        		return Response(serializer.data,
        			status=status.HTTP_201_CREATED)
        	else:
        		return Response(serializer.errors,
        			status=status.HTTP_400_BAD_REQUEST)

		return Response({"msg": "Data is not provided"},
			status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        **Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id, format=None):
        """
        This method checks wheather the request is coming from the admin of the same account.
        It is used to delete existing product from system
        """
        product_object = get_object_or_404(Product, id=id)
        product_object.is_active = False
        product_object.save()
        return Response({'success': True,
                         'msg': 'Product Deleted Successfully'},
                        status=status.HTTP_200_OK) 


# ##########################################################################
# # PLAN CURD API
# ##########################################################################
class PlansList(BaseListCreateAPI):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to add new Plan to system or retrieve existing PLans from system

    Compulsory Fields: plan_type, price, duration

    Filtering Query Params: plan_type, price, duration
    """
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer
    my_filter_fields = ('plan_type', 'price', 'duration',)

    def get_queryset(self):
        """
        This method checks whether the request is coming from the super-admin.
        This method gets the search param and returns the result based on search params.
        If no search params is provided it returns all the plans.
        """
        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True

        queryset = Plans.objects.filter(**filtering_kwargs)
        return queryset

    def post(self, request, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to add new plan to system.
        """
        error_checks = check_for_plan_error(request)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        plan_data = request.data

        plan_data['is_active'] = True
        serializer = PlansSerializer(data=plan_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class PlansDetails(RetrieveUpdateDestroyAPIView):
    """
    Descriptions:
        API is consumed by Admin of App.
        Required SuperUser Login
        API is used to retrive, modify or delete existing Plans from system

    Filtering Query Params: id
    """
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer

    lookup_field = 'id'

    def get(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        This method gives details about a particular account.
        """
        plan_object = get_object_or_404(Plans, id=id,
                                        is_active=True)
        serializer = PlansSerializer(plan_object)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to modify existing Plan from system
        """
        plans_data = request.data
        if plans_data:
            plan_object = get_object_or_404(Plans, id=id,
                                            is_active=True)
            serializer = PlansSerializer(plan_object,
                                         data=plans_data,
                                         partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Data is not provided"},
            status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        """
        **Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id, format=None):
        """
        This method checks whether the request is coming from the super-admin.
        It is used to delete existing plan from system.
        """
        plan_object = get_object_or_404(
            Plans, id=id, is_active=True)
        plan_object.is_active = False
        plan_object.save()
        return Response({'success': True,
                         'msg': 'Plan Deleted Successfully'},
                        status=status.HTTP_200_OK) 


class FunctionalGroupAPIView(APIView):
    """
    Api To display feature list.
    """

    def get(self, request, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = FunctionalGroup.objects.filter(is_active=True)
        serializer = FunctionalGroupSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = request.data
        data["is_active"] = True

        if data:
            error_check = check_for_functional_group_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        serializer = FunctionalGroupSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)


###############################################################################
# BU Unit API view
###############################################################################
class FunctionalGroupRetriveDestroyAPIView(RetrieveDestroyAPIView):


    def get(self, request, id, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = FunctionalGroup.objects.filter(id=id,
            is_active=True)

        if data:
            data = data[0]
            serializer = FunctionalGroupSerializer(data)

            return Response(serializer.data)
        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)

    def delete(self, request, id, format=None):
        """
        This is used to soft delete a Clien Account
        """

        data = FunctionalGroup.objects.filter(id=id)
        if data:
            data = data[0]

            data.is_active = False
            data.save()
            serializer = FunctionalGroupSerializer(data)
     
            return Response(serializer.data)
        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)


    def patch(self, request, id, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = request.data

        if data:
            error_check = check_for_functional_group_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        bu_unit_obj = get_object_or_404(FunctionalGroup,
                                               id=id)
        serializer = FunctionalGroupSerializer(bu_unit_obj, 
                                               data=data,
                                               partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_412_PRECONDITION_FAILED)


class CrmInfoAPIView(APIView):
    """
    This API is used for CURD operation on CRM Info
    """

    def get(self, request, format=None):
        data = CrmInfo.objects.filter(is_active=True)
        serializer = CrmInfoSerializer(data, many=True)
        return Response(serializer.data)

    def patch(self, request, format=None):
        data = request.data

        if data:
            error_check = check_for_crm_info_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        objs = CrmInfo.objects.get(id=data.get('id', ''))
        serializer = CrmInfoSerializer(objs,
                                       data=data,
                                       partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_412_PRECONDITION_FAILED)

    def post(self, request, format=None):

        data = request.data
        data["is_active"] = True

        if data:
            error_check = check_for_crm_info_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        serializer = CrmInfoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)

class CrmDetailView(RetrieveAPIView):

    def get(self, request, id, format=None):

        """
        This mehod is used to get particular crm detail
        if request user is normal user and user is admin
        """

        # crm     = CrmInfo.objects.filter(id=id)
        # user    = request.user

        # if user.role == User.UserTypes.NORMAL_USER.value:
        #     if user.userprofile.is_admin:
        #         account = user.userprofile.bu_unit.account
        #         account = Account.objects.filter(crm_info = crm,
        #             id=account.id)
        # else:
        #     account = Account.objects.filter(crm_info = crm, is_active=True)

        # account_serialize_data = AccountSerializer(account, many=True)

        # return Response(account_serialize_data.data)

        crm_object = get_object_or_404(CrmInfo, id=id,
                                        is_active=True)
        serializer = CrmInfoSerializer(crm_object)
        return Response(serializer.data)

##############################################################################
# Users Feature List
##############################################################################
class FeatureListView(ListAPIView):
    """
    Api To display feature list.
    """

    def get(self, request, format=None):
        """
        Will display Functional Group of requested Users
        """
        # user = request.user
        # response_dict = {}
        # if user.userprofile.bu_unit:
        #     function_list = user.userprofile.bu_unit.functional_group.all()
        #     for i in function_list:
        #         response_dict[i.name.lower().replace(" ", "_")] = True

        # return Response(response_dict)

        response_dict = {}
        function_list = FunctionalGroup.objects.all()
        for i in function_list:
            response_dict[i.name.lower().replace(" ", "_")] = True

        return Response(response_dict)


class BuUnitView(APIView):
    """
    Api To display feature list.
    """

    def get(self, request, format=None):
        """
        Ths API gives details about Client Account.
        """

        # user = request.user
        # if user.role == User.UserTypes.NORMAL_USER.value:
        #     account      = user.userprofile.bu_unit.account
        #     bu_unit_data = BuUnit.objects.filter(is_active=True,
        #         account=account)
        # else:
        #     bu_unit_data = BuUnit.objects.filter(is_active=True)
        # bu_unit_serializer = BuUnitSerializer(bu_unit_data, many=True)
        # return Response(bu_unit_serializer.data)

        bu_unit_data = BuUnit.objects.filter(is_active=True)
        bu_unit_serializer = BuUnitSerializer(bu_unit_data, many=True)
        return Response(bu_unit_serializer.data)


    def patch(self, request, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = request.data

        if data:
            error_check = check_for_bu_unit_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        bu_unit_obj = BuUnit.objects.get(id=data.get('id', ''))
        serializer = BuUnitCreateSerializer(bu_unit_obj,
                                      data=data,
                                      partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_412_PRECONDITION_FAILED)

    def post(self, request, format=None):
        """
        Ths API gives details about Client Account.
        """

        data = request.data
        data["is_active"] = True

        if data:
            error_check = check_for_bu_unit_errors(data)

            if (error_check):
                return Response(error_check,
                                status=status.HTTP_412_PRECONDITION_FAILED)

        serializer = BuUnitCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)


###############################################################################
# BU Unit API view
###############################################################################
class BuUnitRetriveDestroyView(RetrieveDestroyAPIView):

    def get(self, request, id, format=None):
        """
        Ths API gives details about Client Account.
        """

        bu_unit_data = BuUnit.objects.filter(id=id,
            is_active=True)

        if bu_unit_data:
            bu_unit_data = bu_unit_data[0]
            bu_unit_serializer = BuUnitSerializer(bu_unit_data)

            return Response(bu_unit_serializer.data)
        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)

    def delete(self, request, id, format=None):
        """
        This is used to soft delete a Clien Account
        """
        data = request.data

        bu_unit_obj = BuUnit.objects.filter(id=id)
        if bu_unit_obj:
            bu_unit_obj = bu_unit_obj[0]

            bu_unit_obj.is_active = False
            bu_unit_obj.save()
            bu_unit_serializer = BuUnitSerializer(bu_unit_obj)
     
            return Response(bu_unit_serializer.data)
        return Response(error_conf.GENERIC_API_FALIURE,
            status=status.HTTP_412_PRECONDITION_FAILED)


###############################################################################
# BU Unit List API based on Account
###############################################################################
class AccountDetailView(RetrieveAPIView):

    def get(self, request, id, format=None):
        """
        Ths API gives details about Client Account.
        """
        account = Account.objects.get(id=id)
        bu_unit_data = BuUnit.objects.filter(account=account,is_active = True)
        bu_unit_serializer = BuUnitSerializer(bu_unit_data, many=True)

        """
        This code is used for bu unit related user
        """
        # user_data = User.objects.filter(userprofile__bu_unit__in=bu_unit_data, is_active = True)
        # user_serializer = UserDetailSerializer(user_data, many=True)

        functional_data = []
        inactive_functional_data = []
        for data in bu_unit_data:
            functional_data.extend(data.functional_group.all())
        functional_data = set(functional_data)
        functional_data = list(functional_data)

        functional_serializer = FunctionalGroupSerializer(
            functional_data, many=True)

        functional_group = FunctionalGroup.objects.filter(is_active=True)
        for data in functional_group:
            if data not in functional_data:
                inactive_functional_data.append(data)

        inactive_functional_serializer = FunctionalGroupSerializer(
            inactive_functional_data, many=True)

        crm_data = account.crm_info.all()
        active_crm_data = []
        inactive_crm_data = []
        all_crm_data = CrmInfo.objects.filter(is_active = True)
        for crm in all_crm_data:
            if crm in crm_data:
                active_crm_data.append(crm)
            else:
                inactive_crm_data.append(crm)

        active_crm_data_serializer = CrmInfoSerializer(active_crm_data,many=True)
        inactive_crm_data_serializer = CrmInfoSerializer(inactive_crm_data , many=True)

        data = {
            "bu_data": bu_unit_serializer.data,
            # "user": user_serializer.data,
            "active_crm_data": active_crm_data_serializer.data,
            "active_functional_data": functional_serializer.data,
            "inactive_functional_data": inactive_functional_serializer.data,
            "inactive_crm_data":inactive_crm_data_serializer.data
        }

        return Response(data)

class BuUnitDetailView(RetrieveAPIView):

    def get(self, request, id, format=None):

        account_id_list = []
        bu_unit_data = BuUnit.objects.filter(id=id)
        for bu_unit in bu_unit_data:
            account_id = bu_unit.account.id
            account_id_list.append(account_id)
        account = Account.objects.filter(id__in = account_id_list,is_active=True)
        inactive_crm_data = []
        crm_data = []
        active_crm_data_list = []
        all_crm_data = CrmInfo.objects.filter(is_active = True)
        for acc in account:
            crm_data.extend(acc.crm_info.all())
        for data in all_crm_data:
            if (data in crm_data):
                active_crm_data_list.append(data)
            else:
                inactive_crm_data.append(data)
        active_crm_serializer = CrmInfoSerializer(active_crm_data_list, many=True)
        inactive_crm_serializer = CrmInfoSerializer(inactive_crm_data, many=True)
        account_serialize_data = AccountSerializer(account, many=True)

        functional_data = []
        inactive_functional_data = []
        for data in bu_unit_data:
            functional_data.extend(data.functional_group.all())
        functional_data = set(functional_data)
        functional_data = list(functional_data)
        functional_serializer = FunctionalGroupSerializer(
            functional_data, many=True)
        functional_group = FunctionalGroup.objects.filter(is_active=True)
        for data in functional_group:
            if data not in functional_data:
                inactive_functional_data.append(data)

        inactive_functional_serializer = FunctionalGroupSerializer(
            inactive_functional_data, many=True)

        """
        This code is used for bu unit related user
        """
        # user_data = User.objects.filter(userprofile__bu_unit__in=bu_unit_data , is_active = True)
        # user_serializer = UserDetailSerializer(user_data, many=True)

        data = {
            "account":account_serialize_data.data,
            "active_functional_data":functional_serializer.data,
            "inactive_functional_data":inactive_functional_serializer.data,
            "crm_data":active_crm_serializer.data,
            # "user":user_serializer.data,
            "inactive_crm_data":inactive_crm_serializer.data
        }
        return Response(data)

"""
This API list account, functional group, crm, user based on active_tab
"""
class BuUnitGoButtonView(RetrieveAPIView):

    def post(self, request, format=None):

        data                  = request.data
        active_tab            = data.get("active_tab")
        functional_group_list = []
        checkStatus           = data.get("checkedStatus")
        selected_data_id      = data.get('selected_data').get('id')
        crm_data_list = []
        selected_bu_unit      = BuUnit.objects.get(
            id=data.get('selected_bu_unit', {}).get('id'))

        if active_tab == "functional_group":

            already_exist_functional_group = selected_bu_unit.functional_group.all()
            functional_group_list.extend(already_exist_functional_group)

            new_added_functional_group = FunctionalGroup.objects.filter(id = selected_data_id)
            functional_group_list.extend(new_added_functional_group)

            functional_group_list = set(functional_group_list)
            functional_group_list = list(functional_group_list)

            if checkStatus == True:

                if (new_added_functional_group not in already_exist_functional_group):

                    selected_bu_unit.functional_group.add(*functional_group_list)

            if checkStatus == False:

                selected_bu_unit.functional_group.remove(*new_added_functional_group)

            selected_bu_unit.save()
            serializer = BuUnitSerializer(selected_bu_unit)
            return Response(serializer.data,
                                status=status.HTTP_200_OK)

        if active_tab == "crm":

            account_id = selected_bu_unit.account.id
            account = Account.objects.get(id = account_id)

            already_exist_crm = account.crm_info.all()
            crm_data_list.extend(already_exist_crm)

            new_crm_data = CrmInfo.objects.filter(id = selected_data_id)
            crm_data_list.extend(new_crm_data)

            crm_data_list = set(crm_data_list)
            crm_data_list = list(crm_data_list)

            if checkStatus == True:

                if (new_crm_data not in already_exist_crm):

                    account.crm_info.add(*crm_data_list)

            if checkStatus == False:

                account.crm_info.remove(*new_crm_data)

            account.save()
            serializer = AccountSerializer(account)
            return Response(serializer.data,
                        status=status.HTTP_200_OK)

        if active_tab == "user":

            user_data = User.objects.filter(id = selected_data_id)[0]

            if checkStatus == True:
                user_data.is_enable = True
            else:
                user_data.is_enable = False

            user_data.save()
            serializer = UserDetailSerializer(user_data)

            return Response(serializer.data,
                     status= status.HTTP_200_OK)

        if active_tab == "account":
            account = selected_bu_unit.account

            if checkStatus == True:
                account.is_enable = True
            else:
                account.is_enable = False

            account.save()
            serializer = AccountSerializer(account)

            return Response(serializer.data,status = status.HTTP_200_OK)

"""
This api display crm, functional group, bu unti based on selected account data
"""
class AccountGoButtonView(RetrieveAPIView):

    def post(self, request, format=None):
        data = request.data
        selected_account_id = data.get("selected_account")
        checkedStatus = data.get("checkedStatus")
        active_tab = data.get("active_tab")
        selected_data = data.get("selected_data")
        crm_data_list = []

        account_selected = Account.objects.get(
            id=selected_account_id)

        if active_tab == "crm":

            exist_crm_data = account_selected.crm_info.all()
            crm_data_list.extend(exist_crm_data)

            new_crm_data = CrmInfo.objects.filter(
                id=selected_data.get("id"))
            crm_data_list.extend(new_crm_data)

            crm_data_list = set(crm_data_list)
            crm_data_list = list(crm_data_list)

            if checkedStatus == True:
                if(new_crm_data not in exist_crm_data):

                    account_selected.crm_info.add(*crm_data_list)

            if checkedStatus == False:

                account_selected.crm_info.remove(*new_crm_data)

            account_selected.save()
            serializer = AccountSerializer(account_selected)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        if active_tab == "functional_group" :

            functional_group_list = []
            bu_unit = BuUnit.objects.filter(account__id = selected_account_id)

            new_added_functional_group = FunctionalGroup.objects.filter(
                id=selected_data.get("id"))
            functional_group_list.extend(new_added_functional_group)
            for bu in bu_unit:
                already_exist_fun_unit = bu.functional_group.all()
                functional_group_list.extend(already_exist_fun_unit)

                functional_group_list = set(functional_group_list)
                functional_group_list = list(functional_group_list)
                if checkedStatus == True:

                    if (new_added_functional_group not in already_exist_fun_unit):

                        bu.functional_group.add(*functional_group_list)
                        bu.save()

                if checkedStatus == False:
                    bu.functional_group.remove(*new_added_functional_group)
                    bu.save()

            return Response({"success":True},
                                status=status.HTTP_200_OK)

        if active_tab == "bu_unit":

            selected_bu_unit = BuUnit.objects.filter(id = selected_data.get('id'))
            selected_bu_unit = selected_bu_unit[0]

            if checkedStatus == "True":
                selected_bu_unit.is_enable = True

            if checkedStatus == False:
                selected_bu_unit.is_enable = False

            selected_bu_unit.save()
            serializer = BuUnitSerializer(selected_bu_unit)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
"""
This api display crm, functional group, bu unti based on selected user
"""
class UserGoButtonView(RetrieveAPIView):

    def post(self, request, format=None):
        data = request.data
        selected_user_id = data.get("selected_user")
        checkedStatus = data.get("checkedStatus")
        active_tab = data.get("active_tab")
        selected_data = data.get("selected_data")
        fun_grp_list = []
        crm_list = []

        User_selected = UserProfile.objects.get(user__id = selected_user_id)

        if active_tab == "functional_group":

            exist_functinal_group_data = User_selected.bu_unit.functional_group.all()
            fun_grp_list.extend(exist_functinal_group_data)

            new_fun_grp = FunctionalGroup.objects.filter(id = selected_data.get('id'))
            fun_grp_list.extend(new_fun_grp)

            fun_grp_list = set(fun_grp_list)
            fun_grp_list = list(fun_grp_list)

            if checkedStatus == True:
                if(new_fun_grp not in exist_functinal_group_data):
                    User_selected.bu_unit.functional_group.add(*fun_grp_list)

            if checkedStatus == False:
                User_selected.bu_unit.functional_group.remove(*new_fun_grp)

            User_selected.save()
            return Response({"success": True},
                            status=status.HTTP_200_OK)

        if active_tab == "crm":

            exist_crm_data = User_selected.bu_unit.account.crm_info.all()
            crm_list.extend(exist_crm_data)

            new_crm_data = CrmInfo.objects.filter(id = selected_data.get('id'))
            crm_list.extend(new_crm_data)

            crm_list = set(crm_list)
            crm_list = list(crm_list)

            if checkedStatus == True:
                if(new_crm_data not in exist_crm_data):
                    User_selected.bu_unit.account.crm_info.add(*crm_list)

            if checkedStatus == False:
                User_selected.bu_unit.account.crm_info.remove(*new_crm_data)

            User_selected.save()
            return  Response({"success":True},
                             status = status.HTTP_200_OK)

##########################################################################
# API for Flagged Products (AGENT APP)
##########################################################################
class ListFlaggedProductView(ListAPIView):
    """
    Descriptions:
        API is consumed by Agents of App.
        Required Agent Login
        API is used to retrieve existing Flagged Products i.e. product which contains more tickets in system.
    """

    serializer_class = ProductSerializer

    def get(self, request, format=None):

        if request.user.role == User.UserTypes.AGENT.value:
            agent_object = Agent.objects.filter(user=request.user)

            if agent_object:
                flagged_products = {}
                products = []

                categories = agent_object[0].category.all()
                for category in categories:
                    products.extend(Product.objects.filter(
                        organization=agent_object[0].account,
                        category=category))

                product_issue_list = {}
                for product in products:
                    product_ticket = Ticket.objects.filter(
                        is_incident=True,
                        product=product)
                    product_ticket_count = product_ticket.count()
                    if product_ticket_count > product.category.flag_length:
                        issues = []
                        flagged_products[product] = product_ticket_count
                        nlp_product = Nlp_Product.objects.get(
                            name__iexact=product.name)
                        unique_issues = nlp_product.issues.split(';')
                        product_issues = dict.fromkeys(unique_issues, 0)
                        for ticket in product_ticket:
                            issues.extend(ticket.unique_issue.split(','))

                        for issue in issues:
                            if product_issues.get(issue) is not None:
                                product_issues[
                                    issue] = product_issues.get(issue) + 1
                        product_issue_percentage = {}
                        issue_count = sum(product_issues.values())

                        for key, value in product_issues.iteritems():
                            if value > 0:
                                product_issue_percentage[
                                    key] = (value * 100) / issue_count

                        sorted_product_issue_percentage = sorted(
                            product_issue_percentage.items(),
                            key=lambda x: x[
                                1],
                            reverse=True)

                        product_issue_list[
                            product.id] = sorted_product_issue_percentage

                sorted_products = sorted(flagged_products.items(),
                                         key=lambda x: x[1],
                                         reverse=True)

                sorted_flagged_products = [elem[0] for elem in sorted_products]

                serializer = ProductSerializer(sorted_flagged_products,
                                               many=True)
                return Response({"Products": serializer.data,
                                 "issue_percentage": product_issue_list})
        return Response({"msg": "Unauthorized access"},
                        status=status.HTTP_403_FORBIDDEN)    

###############################################################################
# Products Support rating graph (AGENT)
###############################################################################
class ProductSupportRatingView(ListAPIView):
    """
    Descriptions:
        API is consumed by Agents of App.
        Required Agent Login
        API is used to retrieve product support rating score for Support Rating Graph.
    """

    def get(self, request, format=None, **kwargs):
        if request.user.role == User.UserTypes.AGENT.value:
            product_scores = []

            account_tickets = Ticket.objects.filter(
                account=request.user.agent.account,
                reported_date__gt=timezone.now() - timezone.timedelta(days=30),
                is_incident=True)

            account_product = Product.objects.filter(
                organization=request.user.agent.account,
                is_active=True)

            for product in account_product:
                product_values = {}

                product_values['total_count'] = len(
                    account_tickets.filter(
                        product=product,
                        is_incident=True))

                if product_values['total_count'] > 0:
                    product_values['product_name'] = product.name

                    product_values['product_id'] = product.id

                    product_values['support_rating'] = len(
                        account_tickets.filter(
                            product=product,
                            ticket_status=Ticket.TicketStatus.CLOSED.value,
                            is_successful=True))
                    if product_values['total_count']:
                        product_values['colour'] = (
                                                       product_values['support_rating'] * 100) \
                                                   / product_values['total_count']
                    else:
                        product_values['colour'] = 0

                    if product.category.expected_number_of_issues:
                        product_values['issue_percentage'] = (
                                                                 product_values['total_count'] * 100) \
                                                             / product.category.expected_number_of_issues
                    else:
                        product_values['issue_percentage'] = product_values[
                                                                 'total_count'] * 100
                    product_scores.append(product_values)

            product_list = sorted(
                product_scores, key=lambda k: k['issue_percentage'],
                reverse=True)

            if product_list:
                xaxis_data = max(product_list, key=lambda x: x['total_count']).get(
                    'total_count')
                yaxis_data = max(product_list, key=lambda x: x['support_rating']).get(
                    'support_rating')
                xaxis_value, yaxis_value = helper.get_xaxis_yaxis_data(xaxis_data,
                                                                   yaxis_data)
                top_product_id = product_list[0].get('product_id', '')
            else:
                xaxis_value, yaxis_value = 1,1
                top_product_id = None

            product_score_list = product_list[:10]

            result_data = helper.get_support_rating_chart_format(
                product_score_list)

            return Response({'success': True,
                             'result': result_data,
                             'xaxis_value': xaxis_value,
                             'yaxis_value': yaxis_value,
                             'top_product_id': top_product_id},
                            status=status.HTTP_200_OK)
        return Response({'success': False,
                         'msg': 'Only Agents can view performance graph'},
                        status=status.HTTP_403_FORBIDDEN)

###############################################################################
# Top Influencer per product (AGENT)
###############################################################################
class ProductTopInfluencerView(ListAPIView):
    """
    Descriptions:
        API is consumed by Agents of App.
        Required Agent Login
        API is used to view top influencers of a particular product based on it ticket raised on that product.
        In this User Influence score is given 80 per waitage whereas Ticket raised score is given 20 per
    """

    def get(self, request, id, format=None, **kwargs):
        if request.user.role == User.UserTypes.AGENT.value:
            product = Product.objects.filter(
                id=id,
                is_active=True)

            if product:
                results = []
                tickets = Ticket.objects.filter(
                    product=product[0],
                    is_incident=True,
                    reported_date__gt=timezone.now() -
                                      timezone.timedelta(days=30),
                    account=request.user.agent.account)
                """
                Retriving all distinct user's of the product
                """
                users_id = tickets.values_list(
                    'reported_by', flat=True).distinct()
                users = User.objects.in_bulk(users_id).values()
                score = UserScore.objects.all().aggregate(
                    Max('user_score'))
                max_user_score = score.get('user_score__max', 0)
                product_name = product[0].name

                for user in users:
                    user_data = {'user': UserDetailSerializer(user).data}
                    user_score = UserScore.objects.filter(user=user)
                    if user_score:
                        score = user_score[0].user_score
                    else:
                        score = 0
                    """
                    Calculating percentage of user influence with
                    ticket score in 20% and user influence score as 80%
                    """
                    if len(tickets):
                        ticket_influence = (
                                               len(tickets.filter(reported_by=user)) * 20) / len(tickets)
                    else:
                        ticket_influence = 0

                    if max_user_score:
                        user_influence_score = score * 80 / max_user_score
                    else:
                        user_influence_score = 0

                    user_data[
                        'product_influence_percentage'] = ticket_influence + \
                                                          user_influence_score
                    results.append(user_data)

                top_influencers = sorted(
                    results, key=lambda k: k['product_influence_percentage'],
                    reverse=True)[:7]

                return Response({'success': True,
                                 'result': top_influencers,
                                 'product_name': product_name},
                                status=status.HTTP_200_OK)
        return Response({'success': False,
                         'msg': 'Only Agents can view top influencers'},
                        status=status.HTTP_403_FORBIDDEN)


###############################################################################
# BU Unit, Account, Functional Gropup, CRM List API based on User
###############################################################################
class AdminUserDetailView(RetrieveAPIView):

    def get(self, request, id, format=None):
        """
        Ths API gives details required for admin User screen.
        """

        user = User.objects.get(id=id)

        bu_unit_data = user.userprofile.bu_unit
        bu_unit_serializer = BuUnitSerializer(bu_unit_data)

        user_serializer = UserDetailSerializer(user)

        account = bu_unit_data.account

        inactive_functional_data = []
        inactive_crm_data = []
        active_crm_data_list = []
        crm_data = []
        functional_data = bu_unit_data.functional_group.all()

        functional_serializer = FunctionalGroupSerializer(
            functional_data, many=True)

        functional_group = FunctionalGroup.objects.filter(is_active=True)
        for data in functional_group:
            if data not in functional_data:
                inactive_functional_data.append(data)

        inactive_functional_serializer = FunctionalGroupSerializer(
            inactive_functional_data, many=True)

        all_crm_data = CrmInfo.objects.filter(is_active = True)
        crm_data.extend(account.crm_info.all())

        for data in all_crm_data:
            if (data in crm_data):
                active_crm_data_list.append(data)
            else:
                inactive_crm_data.append(data)

        active_crm_serializer = CrmInfoSerializer(active_crm_data_list,many=True)
        inactive_crm_serializer = CrmInfoSerializer(inactive_crm_data,many=True)
        account_serialize = AccountSerializer(account)

        data = {
            "bu_data": bu_unit_serializer.data,
            "user": user_serializer.data,
            "active_crm": active_crm_serializer.data,
            "active_functional_data": functional_serializer.data,
            "inactive_functional_data": inactive_functional_serializer.data,
            "account": account_serialize.data,
            "inactive_crm_data" : inactive_crm_serializer.data
        }

        return Response(data)


###############################################################################
# Account List API based on User and it's user type Normal User
###############################################################################
class AdminAccountFilter(BaseListCreateAPI):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = StandardResultsSetPagination
    my_filter_fields = ('name')

    def get(self, request, format=None):

        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True

        user = self.request.user
        if user.role == User.UserTypes.NORMAL_USER.value:
            acc_id = user.userprofile.bu_unit.account.id
            filtering_kwargs['id'] = acc_id

        account = Account.objects.filter(**filtering_kwargs)
        serializer = AccountSerializer(account, many=True)

        return Response(serializer.data)

###############################################################################
# Bu unit and accoutn list API based on functional group and User 
# and it's user type Normal User
###############################################################################
class FunctinalGroupDetailView(RetrieveAPIView):

    def get(self, request, id, format=None):

        bu_account_id = []
        user          = request.user

        if user.role == User.UserTypes.NORMAL_USER.value:
            if user.userprofile.is_admin:
                account       = user.userprofile.bu_unit.account
                bu_unit = BuUnit.objects.filter(functional_group__id = id,
                    account=account)
        else:
            bu_unit = BuUnit.objects.filter(functional_group__id = id, is_active = True)

        bu_unit_serializer = BuUnitSerializer(bu_unit, many=True)
        for bu in bu_unit:
            bu_account_id.append(bu.account.id)
        account = Account.objects.filter(id__in = bu_account_id, is_active = True)
        account_serializer = AccountSerializer(account, many=True)
        data = {
            "accountData" : account_serializer.data,
            "buUnitData" : bu_unit_serializer.data
            }

        return Response(data)
