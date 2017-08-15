import logging
import uuid
import os
import sys
import requests
from django.conf import settings
from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
    ListAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from private_message_app import error_conf
from private_message_app.helper import export_ticket_chat
from private_message_app.models import (Message)
from private_message_app.serializers import (
    MessageSerializer,
    MessageViewSerializer,
    MessageExportSerializer
)
from private_message_app.system_error import check_for_private_message_error
from private_message_app import error_conf


###############################################################################
# Private Messages Between User and Assigned ticket
###############################################################################
class MessageList(ListCreateAPIView):
    """
    This Class is for Creating and searching
    Message API
    """
    queryset         = Message.objects.all()
    serializer_class = MessageViewSerializer
    
    def get(self, request, format=None, **kwargs):
        """
        This Method Retrieve all the message of given ticket
        if request user is part of same
        """
        data         = request.GET
        ticket_id    = data.get('ticket')
        message_data = Message.objects.filter(ticket=ticket_id)
        serializer   = self.get_serializer(message_data, many=True)
        return Response(serializer.data)    

    def post(self, request, format=None, **kwargs):
        """
        This method checks whether the request is coming
        from the User or Admin and saves
        Message

        Note - In this method, aws cognito user id is saving in sender,
        previously we are saving djagno user id.
        """

        message_data = request.data
        
        error_checks = check_for_private_message_error(request)

        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        message_data['sender'] = uuid.UUID(data.get('user_id'))

        serializer = MessageSerializer(data=message_data)

        if serializer.is_valid():
            message    = serializer.save()
            serializer = MessageViewSerializer(message)
            return Response({"message": serializer.data,
                             "success": True},
                            status=status.HTTP_201_CREATED)
        else:
            logging.info(serializer.errors)
            return Response(error_conf.GENERIC_API_FALIURE,
                            status=status.HTTP_412_PRECONDITION_FAILED)


class MessageActivity(UpdateAPIView):
    """
    This Class is for Creating and searching
    Message API
    """
    queryset         = Message.objects.all()
    serializer_class = MessageSerializer

    def patch(self, request, id, format=None):
        """
        This method checks whether the request is coming
        from the User or Admin and saves
        Message action
        """

        message_data = request.data
        if not message_data.get('action'):
            return Response({"msg": "Action not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        message_obj = Message.objects.get(id=id)

        if message_data['action'] == 'READ':
            message_data['to_user_read'] = True
        elif message_data['action'] == 'UNREAD':
            message_data['to_user_read'] = False
        elif message_data['action'] == 'DELETE':
            message_data['to_user_delete'] = True
        else:
            return Response({"msg": "Unauthorize User"},
                            status=status.HTTP_403_FORBIDDEN)

        del message_data['action']

        serializer = MessageSerializer(message_obj,
                                       data=message_data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class MessageExportView(ListAPIView):
    """
    This view is used to export chat of a particular ticket
    """
    serializer_class = MessageExportSerializer
    queryset = Message.objects.all()

    def get(self, request, id, format=None, **kwargs):

        url='http://%s:%s/api/ticket/%s/' %(settings.HOST,settings.PORT,id)
        ticket_obj=requests.get(url,headers=settings.HEADERS)
        ticket_data = ticket_obj.json()

        if(ticket_obj.status_code==200):
            ticket_messages = Message.objects.filter(ticket=ticket_data['id'])
            export_ticket_chat(ticket_messages, ticket_data, 'private')

            subject = "AUDETEMI (Ticket Private Chat)"
            message = "Chat history of Ticket " + str(ticket_data['description']) + "."

            if 'test' not in sys.argv:
                email_to = ticket_data['reported_by']['email']
                email = EmailMessage(subject, message,
                                     settings.EMAIL_HOST_USER,
                                     [email_to, ])
                email.attach_file(settings.BASE_DIR + "/private_message_app/private-message/" + 'private' + str(ticket_data['id']) + '.pdf')
                email.send()

            return Response({'success': True,
                             'msg': 'Private Chat exported successfully'},
                            status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Ticket does not exist"},
                status=status.HTTP_400_BAD_REQUEST)
