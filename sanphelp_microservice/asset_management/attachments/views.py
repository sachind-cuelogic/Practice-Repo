import os
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from attachments.serializers import AssetsManagementSerializer
from django.shortcuts import render

# Create your views here.
class AssetsManagementCreateView(CreateAPIView):
    serializer_class = AssetsManagementSerializer

    def post(self, request, format=None):
        """
        This method is used to store user's ticket images.
        """

        user_asset_data = request.data
        user_asset_data['created_by'] = 1
        user_asset_data['is_active'] = True
        up_file=request.FILES.get('attachment')
        if up_file:
            destination = open('/var/tmp/' + up_file.name, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()
            try:
                image_obj = open('/var/tmp/' + up_file.name).read()
                file_content = ContentFile(image_obj,
                                           '/var/tmp/' + user_asset_data['name'])
            except:
                return Response({"msg": "Attachment not uploaded successfully."},
                                status=status.HTTP_412_PRECONDITION_FAILED)
            file_content = ContentFile(image_obj,
                                       user_asset_data['name'])
            user_asset_data['attachment'] = file_content
            serializer = AssetsManagementSerializer(data=user_asset_data)

            if serializer.is_valid():
                serializer.save()
                os.remove('/var/tmp/' + up_file.name)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            os.remove('/var/tmp/' + up_file.name)
            return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Attachment not provided"},
                        status=status.HTTP_412_PRECONDITION_FAILED)


class AssetsManagementCreateViewMultipart(CreateAPIView):
    serializer_class = AssetsManagementSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        """
        This method is used to store user's ticket images.
        """
        user_asset_data = request.data

        filename = user_asset_data['name']

        up_file = request.FILES.get('attachment')
        cover_file = request.FILES.get('cover_photo')
        if up_file:
            destination = open('/var/tmp/' + up_file.name, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()
            try:
                image_obj = open('/var/tmp/' + up_file.name).read()
                file_content = ContentFile(image_obj,
                                           '/var/tmp/' + user_asset_data['name'])
            except:
                return Response({"msg": "Attachment not uploaded successfully."},
                                status=status.HTTP_412_PRECONDITION_FAILED)

            if cover_file:
                destination = open('/var/tmp/' + cover_file.name, 'wb+')
                for chunk in cover_file.chunks():
                    destination.write(chunk)
                destination.close()
                try:
                    image_obj = open('/var/tmp/' + cover_file.name).read()
                    cover_file_content = ContentFile(image_obj,
                                                     '/var/tmp/' + user_asset_data['cover_photo_name'])
                    user_asset_data['cover_photo'] = cover_file_content
                except:
                    pass

            user_asset_data['created_by'] = 1
            user_asset_data['is_active'] = True
            user_asset_data['attachment'] = file_content
            serializer = AssetsManagementSerializer(data=user_asset_data)

            if serializer.is_valid():
                serializer.save()
                os.remove('/var/tmp/' + up_file.name)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            os.remove('/var/tmp/' + up_file.name)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Attachment not provided"},
                            status=status.HTTP_412_PRECONDITION_FAILED)
