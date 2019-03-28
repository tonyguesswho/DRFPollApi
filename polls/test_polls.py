from rest_framework.test import APITestCase
#from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from polls import views



class TestPoll(APITestCase):

    def setUp(self):
        #self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.PollsViewset.as_view({'get':'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        #self.client.login(username='test', password='test')

    def test_list(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.uri)
        #response = self.view(request)
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test',email='testuser@gmail.com',password='test')

    def test_create_poll(self):
        self.client.login(username='test', password='test')
        data={
            "question":"who is the king of the jungle",
            "created_by":2
        }
        response = self.client.post(self.uri, data)
        self.assertEqual(response.status_code, 201)



