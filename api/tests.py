import jwt
import bcrypt
import json
from datetime       import datetime

from django.test    import TestCase, Client
from django.conf    import settings

from users.models   import User
from api.models     import Project, Text
from api.test_text  import create_text, patch_text
from api.utils.utils import make_text_obj, preprocess_data

class AiParkAPITest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            id       =1,
            email    ="kim@gamil.com",
            password =bcrypt.hashpw("kim12345!".encode("utf8"),bcrypt.gensalt()).decode("utf8")
        ) 
        Project.objects.create(id=10, user=User.objects.get(id=1), project_title="test", savedpoint="../save")
        complete_preprocess = preprocess_data(create_text.text)
        make_text_obj(user=User.objects.get(id=1), project_id=Project.objects.get(id=10).id, complete_preprocess=complete_preprocess)        
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Project.objects.all().delete()
        Text.objects.all().delete()

    def test_success_create(self):
        """
        프로젝트 -> 텍스트 -> 오디오생성 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id": 1,
                "project_title": "project_first",
                "data" : create_text.text
            }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.post('/api/project', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), True)
        self.assertEqual(response.status_code, 201)

    def test_success_get_list(self):
        """
        프로젝트내 텍스트 조회 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/api/project/10',content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_success_add_text_foward_index(self):
        """
        특정 텍스트 인덱스 앞으로 새로운 텍스트 추가 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
            "data": patch_text.text 
        }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.patch('/api/project/10?index=10', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.json(), True)
        self.assertEqual(response.status_code, 200)
    
    def test_success_delete_project(self):
        """
        프로젝트 삭제 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/api/project/10', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 204)

    def test_success_partial_update(self):
        """
        특정 텍스트 내용변경 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
            "data": "partial update 테스트입니다.",
            "speed": True 
        }
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.put('/api/project/10/index/1', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_success_get_audio_file(self):
        """
        특정텍스트 오디오 파일 전송 성공테스트
        """
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/api/project/10/index/1', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)