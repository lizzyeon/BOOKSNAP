from django.contrib.auth.hashers import make_password
from user.models import User
from django.test import TestCase

# Create your tests here.

class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='test_email@naver.com',
            nickname='test_nickname',
            name='test_name',
            password=make_password('test_password'),
            profile_image = 'default_profile.png')

    def test(self):
        self.assertEqual(1, 1)  # A와 B가 같으면 통과 아니면 실패

    def test_join(self):
        responses = self.client.post('/user/join/', data=dict(
            email='new_email@naver.com',
            nickname='new_nickname',
            name='new_name',
            password='new_password'))
        self.assertEqual(responses.status_code, 200)

        user = User.objects.filter(email="new_email@naver.com").first()

        self.assertEqual(user.nickname, "new_nickname")
        self.assertEqual(user.name, "new_name")
        self.assertTrue(user.check_password("new_password"))

    def test_login(self):
        responses = self.client.post('/user/login/', data=dict(
            email='test_email@naver.com',
            password='test_password'))

        self.assertEqual(responses.status_code, 200)