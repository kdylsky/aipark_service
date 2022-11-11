from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.utils.utils import preprocess_data, make_project_savepoint_obj, make_text_obj, make_audio_obj
from django.db import transaction

class AiParkAPI(APIView):
    def post(self, request, *args, **kwargs):
        return create(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
@transaction.atomic()
def create(request, *args, **kwargs):
    datas = request.data
    complete_preprocess = preprocess_data(datas["data"])
    project_id = make_project_savepoint_obj()
    make_text_obj(project_id,complete_preprocess)
    make_audio_obj(project_id)    
    
    return JsonResponse({"result":"Success"}, status=status.HTTP_201_CREATED)
