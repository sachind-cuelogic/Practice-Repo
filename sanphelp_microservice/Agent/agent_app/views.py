from django.db.models import Sum, Avg, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import status
import json

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from agent_app import system_error
from agent_app.models import Agent
from agent_app.serializers import (
    AgentSerializer,
    AgentUpdateSerializer
)
from agent_app import (
    helper,
    error_conf
)

# from audetemi.custom_pagination import StandardResultsSetPagination
# from knowledgebase.models import Ticket
# from user_auth.models import User
# from user_auth.serializers import UserSerializer, UserUpdateSerializer
# from knowledgebase.serializers import AgentDetailSerializer
# from knowledgebase import helper as knowledgebase_helper
# from accounts.serializers import AccountSerializer,BuUnitSerializer


class CreateAgentUserView(ListCreateAPIView):
    """
    Descriptions:
        API is consumed by SuperAdmin of App or Admin of Account.
        Required SuperUser/Admin Login
        API is used to add new Admin, Agent or Supervisor to particular account.
        API is used to retrieve Admin, Agent or Supervisor.

    Compulsory Fields: account

    Filtering Query Params: account
    """
    """
    Creating API for agent creation which takes user
    details(email, password, confirm_password, first_name
    last_name, phone_number) as input validates the user details and
    creates a agent account.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    my_filter_fields = ['user']

    def get_kwargs_for_filtering(self):
        """
        This is a self defined method for search.
        It searches on the basic of user id.
        If user id is not provided it displays all the agents.

        Note:- the search string should be appended in the urls
        example:- api/agent/register/?user=6
        """
        filtering_kwargs = {}
        for field in self.my_filter_fields:
            # iterate over the filter fields
            # get the value of a field from request query parameter
            field_value = self.request.query_params.get(field)
            # if not self.request.user.is_superuser:
            #     if self.request.user.role == User.UserTypes.NORMAL_USER.value:
            #         return Response(status=status.HTTP_403_FORBIDDEN)
            #     filtering_kwargs['account'] = self.request.user.agent.account
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_queryset(self):
        filtering_kwargs = self.get_kwargs_for_filtering()
        filtering_kwargs['is_active'] = True
        queryset = Agent.objects.filter(**filtering_kwargs)
        return queryset

    def post(self, request):

        data = request.data
        agent_basic_data = data.get('basic_info')
        agent_specific_detail = data.get('agent_info')
        agent_obj = None

        try:
 
            # agent_obj = Agent.objects.get(user=request.user, is_admin=True)

            agent_obj = Agent.objects.get(user=agent_basic_data.get['user'], is_admin=True)

            '''
            As an agent I cannot create another agent
            Only SuperUser can create admin
            '''
            if agent_specific_detail.get('is_admin'):
                return Response({'success': False,
                                 'msg': 'Admin can not create another admin'
                                        ', please contact Superuser for the same.'},
                                status=status.HTTP_412_PRECONDITION_FAILED)

        except Agent.DoesNotExist:
            pass

        if request.user.is_superuser or agent_obj:

            validate_password = helper.get_validate_password(
                    agent_basic_data['password'],
                    agent_basic_data['confirm_password'])
            if not validate_password:
                return Response({'success': False,
                                 'msg': 'validate_password'})

            agent_basic_data['role'] = "Agent"

            del agent_basic_data['confirm_password']
            serializer = UserSerializer(data=agent_basic_data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

            user_id = serializer.data['id']
            user = get_object_or_404(User, id=user_id)
            user.is_email_verified = True
            user.save()

            if not request.user.is_superuser:
                agent_specific_detail['account'] = agent_obj.account.id

            agent_obj = {"is_admin": agent_specific_detail.get('is_admin',
                                                               False),
                         "account": agent_specific_detail.get('account'),
                         "user": user_id,
                         "created_by": request.user.id,
                         "asscendants": agent_specific_detail.get(
                                 'asscendants'),
                         "category": agent_specific_detail.get('category'),
                         "is_active": True,
                         "is_supervisor": agent_specific_detail.get(
                                 'is_supervisor', False)
                         }

            agent_serializer = AgentSerializer(data=agent_obj)
            if agent_serializer.is_valid():
                agent_serializer.save()

                provider = 'Audetemi'
                provider_id = user.id

                helper.add_social_details(user, provider, provider_id)

                return Response({'success': True,
                                 'msg': 'Agent Created Successfully',
                                 'data': agent_serializer.data})
            else:
                user.delete()
                return Response(agent_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "UnAuthorized Access"},
                        status=status.HTTP_403_FORBIDDEN)


# ###############################################################################
# # Update Agent User (AGENT)
# ###############################################################################
# class UpdateAgentUserView(RetrieveUpdateDestroyAPIView):
#     """
#     API for agent information update which takes user
#     details(email, password, confirm_password, first_name
#     last_name, phone_number) as input validates the user details and
#     creates a agent account.
#     """
#     serializer_class = UserSerializer
#     queryset = Agent.objects.all()

#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [IsAuthenticated, IsEmailVerified]

#     def get(self, request, id, format=None):

#         agent_object = get_object_or_404(Agent,
#                                          id=id)
#         serializer = AgentSerializer(agent_object)
#         return Response(serializer.data)

#     def put(self, request, id, format=None):
#         """
#         Put has been disabled.
#         """
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     def patch(self, request, id, format=None):

#         agent_basic_data = request.data.get('basic_info')
#         agent_specific_detail = request.data.get('agent_info')
#         agent_obj = False

#         agent = get_object_or_404(Agent, id=id)

#         current_logged_agent = Agent.objects.filter(user=request.user)

#         if len(current_logged_agent):
#             current_logged_agent = current_logged_agent[0]

#             if current_logged_agent.account != agent.account:
#                 # if agent does not belong to same account 400_BAD_REQUEST it
#                 return Response(status=status.HTTP_400_BAD_REQUEST)

#             # if logged in agent is Admin the he is not allowed to create
#             # another admin
#             if current_logged_agent.is_admin:
#                 if agent_specific_detail.get('is_admin'):
#                     return Response({'success': False,
#                                      'msg': 'Admin cannot assign another admin'
#                                             ', please contact Superuser for the same.'},
#                                     status=status.HTTP_400_BAD_REQUEST)

#             if current_logged_agent.is_supervisor:
#                 # if logged in agent is Supervisor then he is not
#                 # allowed to update a new Admin and Supervisor
#                 if agent_specific_detail.get('is_admin'):
#                     return Response({'success': False,
#                                      'msg': 'Supervisor cannot assign another admin'
#                                             ', please contact Superuser for the same.'},
#                                     status=status.HTTP_400_BAD_REQUEST)

#                 if agent_specific_detail.get('is_supervisor'):
#                     return Response({'success': False,
#                                      'msg': 'Supervisor cannot assign another supervisor'
#                                             ', please contact Admin for the same.'},
#                                     status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     if agent.is_supervisor is True and agent_specific_detail.get('is_supervisor') is False:
#                         return Response({'success': False,
#                                          'msg': 'Supervisor cannot deactivate another supervisor'
#                                                 ', please contact Admin for the same.'},
#                                         status=status.HTTP_400_BAD_REQUEST)
#             if current_logged_agent.id == int(id):
#                 agent_obj = True
#                 serializer = UserUpdateSerializer(
#                         request.user,
#                         data=agent_basic_data,
#                         partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     Response(serializer.errors,
#                              status=status.HTTP_400_BAD_REQUEST)

#             if current_logged_agent.is_admin:
#                 agent_obj = True

#         if request.user.is_superuser or agent_obj:

#             agent_specific_detail['updated_by'] = request.user.id
#             serializer = AgentUpdateSerializer(
#                     agent,
#                     data=agent_specific_detail,
#                     partial=True)

#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,
#                                 status=status.HTTP_200_OK)
#             else:
#                 Response(serializer.errors,
#                          status=status.HTTP_400_BAD_REQUEST)

#         return Response({"msg": "UnAuthorized Access"},
#                         status=status.HTTP_403_FORBIDDEN)

#     def delete(self, request, id, format=None):
#         """
#         Delete has been disabled.
#         """
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ###############################################################################
# # Agent Performance calculation (AGENT)
# ###############################################################################
# class AgentPerformanceView(ListAPIView):
#     """
#     API to view agent performance score, top agents score,
#     Accounts average performance score
#     """
#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [IsAuthenticated, IsEmailVerified]

#     def get(self, request, format=None, **kwargs):
#         if request.user.role == User.UserTypes.AGENT.value:
#             account_agent_scores = []

#             account_tickets = Ticket.objects.filter(
#                     account=request.user.agent.account,
#                     reported_date__gt=timezone.now() - timezone.timedelta(days=30),
#                     ticket_status=Ticket.TicketStatus.CLOSED.value,
#                     is_incident=True)
#             account_average_performance_score = account_tickets.aggregate(
#                     total_heat_index=Sum('heat_index'),
#                     total_count=Count('heat_index'),
#                     average_heat_index=Avg('heat_index'))

#             agents = Agent.objects.filter(account=request.user.agent.account,
#                                           is_active=True)

#             for agent in agents:
#                 tickets = account_tickets.filter(
#                         assign_agent=agent)
#                 account_agent_scores.append(tickets.aggregate(
#                         total_heat_index=Sum('heat_index'),
#                         total_count=Count('heat_index'),
#                         average_heat_index=Avg('heat_index')))
#             highest_agent_score = max(
#                     account_agent_scores, key=lambda x: x['average_heat_index'])

#             agent_tickets = account_tickets.filter(
#                     assign_agent=request.user.agent)
#             agent_performance_score = agent_tickets.aggregate(
#                     total_heat_index=Sum('heat_index'),
#                     total_count=Count('heat_index'),
#                     average_heat_index=Avg('heat_index'))

#             params_send = [highest_agent_score,
#                            agent_performance_score,
#                            account_average_performance_score]
#             xaxis_data = max(params_send, key=lambda x: x['total_count']).get(
#                     'total_count')
#             yaxis_data = max(params_send, key=lambda x: x['average_heat_index']).get(
#                     'average_heat_index')

#             result_data = helper.get_chart_format(params_send)
#             xaxis_value, yaxis_value = helper.get_xaxis_yaxis_data(xaxis_data,
#                                                                    yaxis_data)

#             return Response({'success': True,
#                              'result': result_data,
#                              'xaxis_value': xaxis_value,
#                              'yaxis_value': yaxis_value},
#                             status=status.HTTP_200_OK)
#         return Response({'success': False,
#                          'msg': 'Only Agents can view performance graph'},
#                         status=status.HTTP_403_FORBIDDEN)


# class AdminLoginView(APIView):
#     """
#     Creating API for User Authentication
#     Based On roles and UserName and Passwords
#     Note:-
#     Checks whether the request is from audetemi user
#     by checking the provider name in UserSocialDetails
#     Table and if that entry is primary.
#     """

#     def post(self, request, format=None):
#         """
#         Return a Valid token if username and password
#         is valid for a given client
#         """

#         if request.data:
#             data = request.data

#             error_checks = system_error.check_for_login_input_error(data)

#             if (error_checks):
#                 return Response(error_checks,
#                                 status=status.HTTP_412_PRECONDITION_FAILED)

#             email = data.get('email')
#             password = data.get('password')

#             user = User.objects.get(email=email)
#             username = user.username

#             login_success_data = helper.generate_oauth_token(self, username, password)
#             if login_success_data.status_code != 200:
#                 return Response(error_conf.INVALID_PASSWORD,
#                                 status=status.HTTP_412_PRECONDITION_FAILED)

#             responce_dict = json.loads(login_success_data._content)

#             if user.role == User.UserTypes.NORMAL_USER.value:
#                 serializer = UserSerializer(user)

#             if user.role == User.UserTypes.AGENT.value:
#                 serializer = AgentDetailSerializer(user.agent)

#             responce_dict['personal_info'] = serializer.data

#             return HttpResponse(json.dumps(responce_dict),
#                                 content_type='application/json')

#         return Response(error_conf.NO_INPUT_DATA,
#             status=status.HTTP_400_BAD_REQUEST)


# class AdminHomeSearchView(ListAPIView):

#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [IsAuthenticated, IsEmailVerified]

#     def post(self, request, format=None):

#         search_query = request.data
#         search_type = request.data['search_type']
#         if search_type:

#             if (search_type == "account"):
#                 account = knowledgebase_helper.search_Account(search_query, request)
#                 result = AccountSerializer(account, many=True)
#             elif (search_type == "buUnit"):
#                 buUnit = knowledgebase_helper.search_BuUnit(search_query, request)
#                 result = BuUnitSerializer(buUnit, many=True)
#             else:
#                 search_string = search_query.get("search_string")
#                 user = User.objects.filter(
#                     Q(full_name__icontains = search_string) | Q(email__icontains = search_string))

#                 result = UserSerializer(user, many=True)

#             return Response(result.data,
#                         status=status.HTTP_200_OK)

#         return Response(error_conf.SELECT_OPTION,
#                         status=status.HTTP_400_BAD_REQUEST)


# class UpdateAgentAccountView(ListAPIView):

#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [IsAuthenticated, IsEmailVerified]

#     def post(self, request, format=None):

#         ticket_id = request.data.get('ticket_id')
#         user = request.user
#         if ticket_id:
#             if user.role == User.UserTypes.AGENT.value:
#                 current_logged_agent = Agent.objects.filter(user=request.user)
#                 if current_logged_agent:
#                     current_logged_agent = current_logged_agent[0]
#                     ticket = Ticket.objects.get(id=ticket_id)
#                     current_logged_agent.account = ticket.account
#                     current_logged_agent.save()
#             return Response({'success': True},
#                         status=status.HTTP_200_OK)

#         return Response(error_conf.SELECT_OPTION,
#                         status=status.HTTP_400_BAD_REQUEST)
