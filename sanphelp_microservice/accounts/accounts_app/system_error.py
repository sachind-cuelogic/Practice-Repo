from accounts_app import error_conf
from accounts_app.models import (
    BuUnit,
    Account
)
from rest_framework.parsers import JSONParser

def check_for_industry_error(request):
	"""
	Error Handling For Private Message API
	"""
	data = request.data

	if data.get('name'):
		if not data.get('created_by'):
			return error_conf.CREATED_BY_IS_REQUIRED
		if not data.get('updated_by'):
			return error_conf.UPDATED_BY_IS_REQUIRED

		return False	
	else:

		return error_conf.CANNOT_POST_EMPTY_NAME

def check_for_account_error(request):

	data = request.data

	if data.get('name'):
		if not data.get('created_by'):
			return error_conf.CREATED_BY_IS_REQUIRED
		if not data.get('updated_by'):
			return error_conf.UPDATED_BY_IS_REQUIRED
		if len(Account.objects.filter(name__iexact=data.get("name")).exclude(id=data.get('id'))):
			return error_conf.ACCOUNT_NAME_ALREADY_EXISTS

		if len(Account.objects.filter(code__iexact=data.get("code")).exclude(id=data.get('id'))):
			return error_conf.ACCOUNT_CODE_ALREADY_EXISTS

		return False	
	else:

		return error_conf.CANNOT_POST_EMPTY_NAME	


def check_for_category_error(request):
	data = request.data

	if data.get('name'):
		if not data.get('created_by'):
			return error_conf.CREATED_BY_IS_REQUIRED
		if not data.get('updated_by'):
			return error_conf.UPDATED_BY_IS_REQUIRED
		if not data.get('organization'):
			return error_conf.ORGANISATION_IS_NOT_PROVIDED
		return False	
	else:

		return error_conf.CANNOT_POST_EMPTY_NAME	


def check_for_product_error(request):

	data = request.data
	if data.get('name'):
		if not data.get('created_by'):
			return error_conf.CREATED_BY_IS_REQUIRED
		if not data.get('updated_by'):
			return error_conf.UPDATED_BY_IS_REQUIRED
		if not data.get('organization'):
			return error_conf.ORGANISATION_IS_NOT_PROVIDED
		if not data.get('category'):
			return error_conf.CATEGORY_IS_NOT_PROVIDED		
		return False	
	else:

		return error_conf.CANNOT_POST_EMPTY_NAME	


def check_for_plan_error(request):
	data = request.data

	if data.get('plan_type'):
		if not data.get('created_by'):
			return error_conf.CREATED_BY_IS_REQUIRED
		if not data.get('updated_by'):
			return error_conf.UPDATED_BY_IS_REQUIRED
		if not data.get('price'):
			return error_conf.PRICE_IS_NOT_PROVIDED
		if not data.get('duration'):
			return error_conf.DURATION_IS_NOT_PROVIDED		
		return False	
	else:
		return error_conf.CANNOT_POST_EMPTY_NAME

def check_for_bu_unit_errors(data):
    """
	Error Handling BU Unit Create And Update
    """

    if len(BuUnit.objects.filter(name = data.get('name')).exclude(id=data.get('id'))) != 0:
            return error_conf.BU_NAME_ALREADY_EXISTS

    if len(BuUnit.objects.filter(code = data.get('code')).exclude(id=data.get('id'))) != 0:
        return error_conf.BU_CODE_ALREADY_EXISTS

    return False


def check_for_functional_group_errors(data):
	
	"""
	Error Handling Functional Group Create And Update
	"""

	if len(BuUnit.objects.filter(name = data.get('name'),is_active=True).exclude(id=data.get('id'))) != 0:
		return error_conf.FUNCTIONAL_GROUP_NAME_ALREADY_EXISTS

	return False


def check_for_crm_info_errors(data):
	return False


def validate_create_account_data(data):
    if len(Account.objects.filter(name__iexact=data.get("name")).exclude(id=data.get('id'))):
        return error_conf.ACCOUNT_NAME_ALREADY_EXISTS

    if len(Account.objects.filter(code__iexact=data.get("code")).exclude(id=data.get('id'))):
        return error_conf.ACCOUNT_CODE_ALREADY_EXISTS

    return False
