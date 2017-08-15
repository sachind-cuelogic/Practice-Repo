from django.shortcuts import get_object_or_404
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mobile_notifications_app.custom_pagination import StandardResultsSetPagination
from mobile_notifications_app import utils
from mobile_notifications_app.models import UserNotifications, UserBadgeCount
from mobile_notifications_app.serializers import (RegisterIOSDeviceSerializer,
                                              RegisterAndroidDeviceSerializer,
                                              UserNotificationsSerializer,
                                              UserBadgeCountSerializer, UserReadNotificationsSerializer)

# Create your views here.
class RegisterIOSDevice(generics.CreateAPIView):
    """
    API for Creating OTP
    For a given Phone Number
    """
    queryset = APNSDevice.objects.all()
    serializer_class = RegisterIOSDeviceSerializer

    def post(self, request, *args, **kwargs):
        mob_noty_data = request.data

        mob_noty_data['registration_id'] = mob_noty_data.get('device_token')

        if len(APNSDevice.objects.filter(registration_id=mob_noty_data['registration_id'])):
            return Response({
                "msg": "Device Already registered"
            }, status=status.HTTP_200_OK)

        mob_noty_data['active'] = True
        serializer = RegisterIOSDeviceSerializer(data=mob_noty_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'msg': 'Device Successfully Registered for notifications'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_412_PRECONDITION_FAILED
            )

class ModifyIOSDevice(generics.UpdateAPIView):
    '''
    This API will modify the IOS device
    '''
    queryset = APNSDevice.objects.all()
    serializer_class = RegisterIOSDeviceSerializer

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        mob_noty_data = request.data
        # following line is dependent on user service
        #mob_noty_data['user'] = request.user.id
        mob_noty_data['active'] = True
        mob_dev_obj = get_object_or_404(
            APNSDevice,
            registration_id=mob_noty_data['device_token'])
        serializer = RegisterIOSDeviceSerializer(mob_dev_obj,
                                                 data=mob_noty_data,
                                                 partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'msg': 'Mobile Successfully Updated for notifications'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_412_PRECONDITION_FAILED
            )

class RemoveIOSDevice(generics.DestroyAPIView):
    '''
    This API will remove the IOS device 
    '''
    queryset = APNSDevice.objects.all()
    serializer_class = RegisterIOSDeviceSerializer

    def delete(self, request, *args, **kwargs):
        mob_noty_data = request.data
        mob_dev_obj = get_object_or_404(
            APNSDevice,
            registration_id=mob_noty_data['device_token'])

        mob_dev_obj.active = False
        mob_dev_obj.user = None
        mob_dev_obj.save()
        return Response({'success': True,
                         'msg': 'User Removed from Recieving Mobile Notifications'})

class RegisterAndroidDevice(generics.CreateAPIView):
    """
    API for Creating OTP
    For a given Phone Number
    """
    queryset = GCMDevice.objects.all()
    serializer_class = RegisterAndroidDeviceSerializer

    def post(self, request, *args, **kwargs):
        mob_noty_data = request.data

        mob_noty_data['registration_id'] = mob_noty_data.get('device_token')

        if len(GCMDevice.objects.filter(registration_id=mob_noty_data['registration_id'])):
            return Response({
                "msg": "Device Already registered"
            }, status=status.HTTP_200_OK)

        mob_noty_data['active'] = True
        serializer = RegisterAndroidDeviceSerializer(data=mob_noty_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'msg': 'Mobile Successfully Registered for notifications'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_412_PRECONDITION_FAILED
            )
class ModifyAndroidDevice(generics.UpdateAPIView):
    '''
    This API will modify the android mobile device
    '''
    queryset = GCMDevice.objects.all()
    serializer_class = RegisterAndroidDeviceSerializer

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        mob_noty_data = request.data
        # this line is dependent on user_Service
        #mob_noty_data['user'] = request.user.id
        mob_noty_data['active'] = True
        mob_dev_obj = get_object_or_404(
            GCMDevice,
            registration_id=mob_noty_data['device_token'])
        serializer = RegisterAndroidDeviceSerializer(mob_dev_obj,
                                                     data=mob_noty_data,
                                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'msg': 'Mobile Successfully Updated for notifications'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_412_PRECONDITION_FAILED
            )

class RemoveAndroidDevice(generics.DestroyAPIView):
    '''
    This API will remove android device
    '''
    queryset = GCMDevice.objects.all()
    serializer_class = RegisterAndroidDeviceSerializer

    def delete(self, request, *args, **kwargs):
        mob_noty_data = request.data
        mob_dev_obj = get_object_or_404(
            GCMDevice,
            registration_id=mob_noty_data['device_token'])

        mob_dev_obj.active = False
        mob_dev_obj.user = None
        mob_dev_obj.save()
        return Response({'success': True,
                         'msg': 'User Removed from Recieving Mobile Notifications'})

class GetUserNotifications(ListAPIView):
    '''
    This API will serve all the notification of a particular user
    on mobile
    '''
    serializer_class = UserNotificationsSerializer
    queryset = UserNotifications.objects.all()
    pagination_class = StandardResultsSetPagination
    my_filter_fields = ('notification_type',)

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

    def get_queryset(self):
        filtering_kwargs = self.get_kwargs_for_filtering()
        #filtering_kwargs['user'] = self.request.user
        queryset = UserNotifications.objects.filter(**filtering_kwargs).order_by('-reported_date')
        return queryset

class MarkUserNotificationsRead(UpdateAPIView):
    '''
    This API wil change the read unread status of a
    particular notification
    '''
    serializer_class = UserReadNotificationsSerializer
    queryset = UserNotifications.objects.all()
    pagination_class = StandardResultsSetPagination

    def put(self, request, format=None):
        """
        Put has been disabled.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        notification_data = request.data
        notification_id = notification_data.get('id')
        notification_data['is_read'] = True
        notification_object = get_object_or_404(UserNotifications,
                                                id=notification_id)
        serializer = UserNotificationsSerializer(notification_object,
                                                 data=notification_data,
                                                 partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Notification Has been marked read by user'})
        Response({'msg': serializer.errorrs}, status=status.HTTP_412_PRECONDITION_FAILED)

class GetUserBadgeCount(ListAPIView):
    '''
    This API will be called first time user logged in system
    This API will count of unread notification to user
    '''
    serializer_class = UserBadgeCountSerializer
    queryset = UserBadgeCount.objects.all()

    def get(self, request, *args, **kwargs):
        #this part is dependent on user service
        user_badge_obj = UserBadgeCount.objects.filter(user=1)
        if user_badge_obj:
            return Response({'badge_count': user_badge_obj[0].badge_count},
                            status=status.HTTP_200_OK)
        return Response({'badge_count': 0},
                        status=status.HTTP_200_OK)

class ResetUserBadgeCount(UpdateAPIView):
    '''
    This API will reset badge count on receiving reset request.
    '''
    serializer_class = UserBadgeCountSerializer
    queryset = UserBadgeCount.objects.all()

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        #this is dependent on user_Service
        user_badge_obj = UserBadgeCount.objects.filter(user=1)
        if user_badge_obj:
            data = {"badge_count": 0}
            serializer = UserBadgeCountSerializer(user_badge_obj[0], data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
        return Response({"msg": "badge count has been reset"},
                        status=status.HTTP_200_OK)

class SendDummyNotification(ListAPIView):
    '''
    This API is writtern for temp sending of scenarios
    notification on mobile
    '''

    def get(self, request, *args, **kwargs):
        notification_type = UserNotifications.NotificationType.USER_SCENARIOS.value
        msg = "Alert recieved from your car"
        #this part is dependent on user_Service
        # utils.send_dummy_notification(User.objects.filter(**{'role': User.UserTypes.NORMAL_USER.value}),
        #                               msg,
        #                               {"notification_type": notification_type,
        #                                "unique_id": 1
        #                                })
        return Response({"success": True},
                        status=status.HTTP_200_OK)

class SendComponentNotification(ListAPIView):
    '''
    This API is writtern for temp sending of scenarios
    notification on mobile
    '''

    def get(self, request, *args, **kwargs):
        notification_type = UserNotifications.NotificationType.COMPONENT_FAILURE.value
        msg = "Component failure alert recieved for your car."
        #this part is dependent on user_Service
        # utils.send_dummy_notification(
        #     User.objects.filter(**{'role': User.UserTypes.NORMAL_USER.value}),
        #     msg,
        #     {"notification_type": notification_type,
        #      "unique_id": 1
        #      })
        return Response({"success": True},
                        status=status.HTTP_200_OK)
