from http.client import responses

from django.test import TestCase

# Create your tests here.

class UserTest(TestCase):
    def test(self):
        self.assertEqual(1, 1)  # A와 B가 같으면 통과 아니면 실패

    def test_join(self):
        responses = self.client.post('/user/join', data=dict(
            email='test_email@naver.com',
            nickname='test_nickname',
            name='test_name',
            password='test_password'), follow='True')
        self.assertEqual(responses.status_code, 200)


