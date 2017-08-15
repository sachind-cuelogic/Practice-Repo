# Create your views here.
import sys
import requests
import json
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)

from rest_framework.response import Response

from comment_app import error_conf

from comment_app.helper import export_ticket_chat
from comment_app.models import (
    Comments,
    CommentAndVote,
)
from comment_app.serializers import (
    CommentSerializer,
    ListCommentAndVoteSerializer,
    UserCommentListSerializer,
    CommentAndVoteSerializer,
)
from comment_app.custom_pagination import StandardResultsSetPagination
from comment_app.system_errors import check_for_public_message_error

# Create your views here.
class CommentCreateView(ListCreateAPIView):
    """
    This API is used to get list of comments on
    a particular ticket and create a comment.
    """

    serializer_class = UserCommentListSerializer
    my_filter_fields = ('ticket',)
    pagination_class = StandardResultsSetPagination

    def get_kwargs_for_filtering(self):
        """
        This is a self defined method for search.
        It searches on the basic of Ticket.
        It displays all the comment under one
        Ticket.

        Note:- the search string should be appended in the urls
        example:- /api/comment/?ticket=1
        """
        
        filtering_kwargs = {}
        for field in self.my_filter_fields:
            """
            iterate over the filter fields
            get the value of a field from request query parameter
            """            
            field_value = self.request.query_params.get(field)
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_queryset(self):

        filtering_kwargs = self.get_kwargs_for_filtering()
        if not filtering_kwargs:
            return Comments.objects.none()
        filtering_kwargs['is_active'] = True
        queryset = Comments.objects.filter(
            **filtering_kwargs).order_by('-created_at')
        return queryset

    def post(self, request, format=None):
        """
        This method checks wheather the request is coming
        from the an agent or a normal user. If so then
        comment is created.
        """
        comment_data = request.data
        comment_data['user'] = 1
        comment_data['is_active'] = True

        if comment_data.get('ticket'):

            """ 
            This part is depends on ticket_service
            This url will call get ticket API of Audetemi main project
            for check whether ticket exist of not and get ticket object.  
            """
            # url='http://%s:%s/api/ticket/%s/' %(settings.HOST,settings.PORT,comment_data['ticket'])
            # ticket_obj=requests.get(url,headers=settings.HEADERS)

            # if ticket_obj.status_code==200: 
            # ticket_obj=ticket_obj.json()

            error_checks = check_for_public_message_error(request)
            if error_checks:
                return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

            serializer = CommentSerializer(data=comment_data)

            if serializer.is_valid():
                comment = serializer.save()

                serializer = UserCommentListSerializer(
                    comment,
                    context={"request": request})

                total_count = len(Comments.objects.filter(ticket= comment_data['ticket'],
                                                          is_active=True))
                return Response({'success': True,
                                 'msg': 'Successfully commented',
                                 'total_count': total_count,
                                 'comment': serializer.data},
                                status=status.HTTP_200_OK)
            logging.info(serializer._errors)
            return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_400_BAD_REQUEST)
            """
            If ticket object does not exist will give error message
            """
            # return Response(error_conf.GENERIC_API_FALIURE,
            #                 status=status.HTTP_400_BAD_REQUEST)
        return Response(error_conf.TICKET_NOT_PROVIDED,
                        status=status.HTTP_412_PRECONDITION_FAILED)
    

###############################################################################
# Comment Update Delete Get API
###############################################################################
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    This API is used to upadte, soft delete and view details of
    a particular comment.
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'

    def get(self, request, id, format=None):
        """
        This method shows detail of a particular
        comment.
        """

        comment_object = get_object_or_404(Comments,
                                           id=id,
                                           is_active=True)
        serializer = UserCommentListSerializer(
            comment_object,
            context={"request": request})
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        """
        This method checks wheather the request is coming
        from the user which has created the comment and edits
        that particular comment.
        """
        comment_object = get_object_or_404(Comments,
                                           id=id)
        comment_data = request.data
        serializer = CommentSerializer(comment_object,
                                       data=comment_data,
                                       partial=True)
        if serializer.is_valid():
            comment = serializer.save()

            serializer = UserCommentListSerializer(
                comment,
                context={"request": request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,id,format=None):
        """
        Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id, format=None):
        """
        This method checks wheather the request is coming
        from the user which has created the comment and soft
        deletes it.
        """

        comment_object = get_object_or_404(Comments,
                                           id=id)
        comment_object.is_active = False
        comment_object.save()
        return Response({'success': True,
                         'msg': 'Comment Deleted Successfully'})

###############################################################################
# Comment Like/Upvote API
###############################################################################
class CommentVoteView(ListCreateAPIView):
    """
    This API is used to liked/DisLiked
    a particular comment.
    """
    serializer_class = ListCommentAndVoteSerializer
    my_filter_fields = ('comment',)

    def get_kwargs_for_filtering(self):
        """
        This is a self defined method for search.
        It searches on the basic of comment.
        If name is not provided it displays all the likes.
        Note:- the search string should be appended in the urls
        example:- /api/comment/like/?comment=7
        """
        filtering_kwargs = {}
        for field in self.my_filter_fields:
            """
            iterate over the filter fields
            get the value of a field from request query parameter
            """

            field_value = self.request.query_params.get(field)
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_queryset(self):
        filtering_kwargs = self.get_kwargs_for_filtering()
        queryset = CommentAndVote.objects.filter(**filtering_kwargs)
        return queryset

    def post(self, request, format=None):
        """
        This method checks wheather the request is coming
        from a normal user. If so then
        comment is liked/DisLiked.
        """
        upvote_data = request.data

        comment_vote_object = CommentAndVote.objects.filter(
            comment=upvote_data['comment'],
            user=1
        )

        if not len(comment_vote_object):
            upvote_data['user'] = 1
            serializer = CommentAndVoteSerializer(data=upvote_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True,
                                 'user_liked': True})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            comment_vote_object[0].delete()
            return Response({'success': True,
                             'user_liked': False})


# ###############################################################################
# # Ticket comments Export as Email API (AGENT)
# ###############################################################################
class CommentExportView(ListAPIView):
    """
    This view is used to export chat of a particular ticket
    """
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    def get(self, request, id, format=None, **kwargs):

        url='http://%s:%s/api/ticket/%s/' %(settings.HOST,settings.PORT,id)
        ticket_obj=requests.get(url,headers=settings.HEADERS)
        if ticket_obj.status_code==200:
            ticket_obj=ticket_obj.json()
            ticket_messages = Comments.objects.filter(ticket=ticket_obj['id'])

            export_ticket_chat(ticket_messages,ticket_obj,id, 'public')

            subject = "Ticket's Comments"
            message = "comments history of Ticket has been attached"

            if 'test' not in sys.argv:
                email_to =  ticket_obj['assign_agent']['email']#request.user.email
                email = EmailMessage(subject, message,
                                     settings.EMAIL_HOST_USER,
                                     [email_to, ])
                email.attach_file(
                    settings.BASE_DIR + "/comment_app/public-message/" + 'public' + str(id) + '.pdf')
                email.send()
            """
            Deletes the file after chat mail has been sent /comment_app/public-message/
            """
            #os.remove(settings.BASE_DIR + "/comment_app/public-message/" + 'public' + str(id) + '.pdf')

            return Response({'success': True,
                             'msg': 'Comments exported successfully'},
                            status=status.HTTP_200_OK)
            
        return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_400_BAD_REQUEST)
