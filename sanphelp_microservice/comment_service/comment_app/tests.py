from django.test import TestCase
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from comment_app.models import Comments
from comment_app import views

###############################################################################
# Comment's Test Case
###############################################################################
class CommentTests(APITestCase):
    """
    TestCase to test comment create, update, delete and retrive
    """

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.comments = Comments.objects.create(
                ticket=2,
                is_active=True,
                user=1,
                comment_text="Demo comment"
        )

    def test_comment_create(self):
        """
        Test case for comment on ticket
        """
        url = '/api/comment/'
        data = {
            "comment_text": "Hey my sixth comment",
            "ticket": 2
        }
        factory = APIRequestFactory()
        view = views.CommentCreateView.as_view()
        request = factory.post(url, data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_comment_create_fail(self):
        """
        Test case for comment on ticket
        """
        url = '/api/comment/'
        data = {
            "comment_text": "Hey my sixth comment",
            "ticket": 100
        }
        factory = APIRequestFactory()
        view = views.CommentCreateView.as_view()
        request = factory.post(url, data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)


    def test_comment_get(self):
        """
        Test case for comment on ticket
        """
        url = '/api/comment/1/'
        factory = APIRequestFactory()
        view = views.CommentDetailView.as_view()
        request = factory.get(url, format='json')
        response = view(request, id=Comments.objects.all()[0].id)
        self.assertEqual(response.status_code, 200)

    def test_comment_get_fail(self):
        """
        Test case for comment on ticket
        """
        url = '/api/comment/100/'
        factory = APIRequestFactory()
        view = views.CommentDetailView.as_view()
        request = factory.get(url, format='json')
        response = view(request, id=100)
        self.assertEqual(response.status_code, 404)


    def test_comment_update(self):
        """
        Test case for update comment on ticket
        """
        url = '/api/comment/1/'
        data = {
            "comment_text": "Hey my update comment"
        }
        factory = APIRequestFactory()
        view = views.CommentDetailView.as_view()
        request = factory.patch(url, data=data, format='json')
        response = view(request, id=self.comments.id)
        self.assertEqual(response.status_code, 201)

    def test_comment_delete(self):
        """
        Test case for delete comment on ticket
        """
        url = '/api/comment/1/'
        factory = APIRequestFactory()
        view = views.CommentDetailView.as_view()
        request = factory.delete(url, format='json')
        response = view(request, id=self.comments.id)
        self.assertEqual(response.status_code, 200)

    def test_comment_like(self):
        """
        Test case for like comment on ticket
        """
        url = '/api/comment/like/'
        data = {
            "comment": self.comments.id
        }
        factory = APIRequestFactory()
        view = views.CommentVoteView.as_view()
        request = factory.post(url, data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_comment_export(self):
        """
        Test case for export comment on ticket
        """
        url = '/api/comments/export/1/'
        factory = APIRequestFactory()
        view = views.CommentVoteView.as_view()
        request = factory.get(url)
        response = view(request)
        self.assertEqual(response.status_code, 200)
