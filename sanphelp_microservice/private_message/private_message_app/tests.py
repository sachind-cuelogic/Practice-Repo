from django.test import TestCase
from django.test import RequestFactory

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from private_message_app.models import Message
from private_message_app import views

class PrivateMessageTests(APITestCase):
    """
    TestCase to test comment create, update, delete and retrive
    """

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        self.message = Message.objects.create(
            ticket=1,
            message_text="This is private message on ticket",
            sender=1,
            receiver=2
        )

    def test_message_create(self):
        """
        Test case for comment on ticket
        """

        url = '/api/private-message/'
        data = {
          "ticket":1,
          "sender":"1",
          "receiver":"2",
          "message_text":"this is test private message"
        }

        factory = APIRequestFactory()
        view = views.MessageList.as_view()

        request = factory.post(url, data=data, format='json')
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_message_create_fail(self):
        """
        Test case for post comment on ticket
        """

        url = '/api/private-message/'
        data = {
          "sender":"1",
          "receiver":"2",
          "message_text":"this is test private message"
        }

        factory = APIRequestFactory()
        view = views.MessageList.as_view()

        request = factory.post(url, data=data, format='json')
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, 400)


    def test_message_get(self):
        """
        Test case for get comment on ticket
        """

        url = '/api/private-message/?ticket=1'
        factory = APIRequestFactory()
        view = views.MessageList.as_view()

        request = factory.get(url, format='json')
        force_authenticate(request)
        response = view(request, id=Message.objects.all()[0].id)
        self.assertEqual(response.status_code, 200)

    def test_message_get_fail(self):
        """
        Test case for comment on ticket fail
        """
        
        url = '/api/private-message/?ticket=100'
        factory = APIRequestFactory()
        view = views.MessageList.as_view()

        request = factory.get(url, format='json')
        force_authenticate(request)
        response = view(request, id=Message.objects.all()[0].id)
        self.assertEqual(response.status_code, 400)

    def test_comment_update(self):
        """
        Test case for update comment on ticket
        """
        url = '/api/private-message/update/1'
        data = {
            
            "message_text":"Hi am sachin",
            "action":"READ"
        }
        factory = APIRequestFactory()
        view = views.MessageActivity.as_view()

        request = factory.patch(url, data=data, format='json')
        force_authenticate(request)
        response = view(request, id=self.message.id)
        self.assertEqual(response.status_code, 200)

    def test_export_ticket_message_get(self):
        """
        Test Case to export message of a ticket
        """
        url = '/api/private-message/export/1'
        factory = APIRequestFactory()
        view = views.MessageExportView.as_view()

        request = factory.get(url, format='json')
        force_authenticate(request)
        response = view(request, id=1)
        self.assertEqual(response.status_code, 200)
