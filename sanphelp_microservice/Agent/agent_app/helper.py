from random import randint

import pdfkit
import requests
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

# from attachments.models import AssetsManagement
# from core.models import OTPGenerator
# from knowledgebase.models import Ticket
# from nlp_analysis import nlp_helper
# from user_auth.models import User
# from user_details.models import UserSocialDetails


###############################################################################
# Function to validate OTP
###############################################################################
def get_validate_password(password, confirm_password):
    """
    Password Rules Followed.
    a) Password should have a minimum length of 8
    b) Password must contains one Numeric Character
    c) Password must contain one alpha character
    """

    min_length = 8
    if password == confirm_password:

        # check if password length is greater than 8
        # check for digit in password
        # check for letters in password
        if len(password) >= min_length:
            # if any(char.isdigit() for char in password) \
            #         and any(char.isalpha() for char in password):
            #     return True
            # else:
            #     return False
            return True
    return False

###############################################################################
# Function will format the data accordingly for chart
###############################################################################
def get_chart_format(data=None):
    result_data = []
    counter = -1

    for entity in data:

        counter += 1
        if counter == 0:
            agent_name = {"v": "Top Agent"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v": 0}

        elif counter == 1:
            agent_name = {"v": "You"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v": 1}

        else:
            agent_name = {"v": "Average"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v": 2}

        agent_total_ticket_count = {
            "v": entity.get('total_count', 0) if entity.get('total_count') else 0}

        agent_performance = {
            "c": [agent_name, agent_total_ticket_count,
                  agent_average_score, agent_color]}
        result_data.append(agent_performance)
    return result_data


###############################################################################
# Function will get xaxis and yaxis data for representing graph
###############################################################################
def get_xaxis_yaxis_data(xaxis_data=0, yaxis_data=0):
    if xaxis_data:
        xaxis_data += (xaxis_data * 25) / 100
    else:
        xaxis_data = 0
    if yaxis_data:
        yaxis_data += (yaxis_data * 25) / 100
    else:
        yaxis_data = 0
    return (xaxis_data, yaxis_data)    



def search_Account(search_query, request):

    search_string = str(search_query.get("search_string"))
    account = []

    if request.user.role == User.UserTypes.NORMAL_USER.value:
        if request.user.userprofile.bu_unit:
            account = Account.objects.filter(name=request.user.userprofile.bu_unit.account.name)
    else:
        account = Account.objects.filter(
            Q(name__icontains = search_string) | Q(
                code__icontains = search_string))

    return account


def search_BuUnit(search_query, request):

    search_string = str(search_query.get("search_string"))
    buUnit = []

    if request.user.role == User.UserTypes.NORMAL_USER.value:
        if request.user.userprofile.bu_unit:
            buUnit = BuUnit.objects.filter(
                Q(name__icontains = search_string,
                    account=request.user.userprofile.bu_unit.account) | Q(
                    code__icontains = search_string,
                    account = request.user.userprofile.bu_unit.account))
    else:
        buUnit = BuUnit.objects.filter(
            Q(name__icontains = search_string) | Q(code__icontains = search_string))

    return buUnit
