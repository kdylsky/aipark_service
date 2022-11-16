import jwt
import json
import bcrypt
from datetime     import datetime

from django.test  import TestCase, Client
from django.conf  import settings

from users.models import User

class SignUpTest(TestCase):
    def test_success_signup(self):
        """
        회원가입 성공 테스트
        """
        client = Client()
        data = {
            "id" : 1,
            "email":"lee@naver.com",
            "password":"lee12345!"
        }
        response = client.post("/user/signup", data=json.dumps(data), content_type='application/json') 
        self.assertEqual(response.status_code, 201)


class LoginInAPITest(TestCase):
    def setUp(self):
        User.objects.create(id=1 ,email="kim@naver.com",password=bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8"))

    def tearDown(self):
        User.objects.all().delete()
    
    def test_success_login(self):
        """
        로그인 성공 테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" :1,
                "email": "kim@naver.com",
                "password" : "kim12345!"
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/user/login', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)