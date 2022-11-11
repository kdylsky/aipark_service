from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.utils.utils import preprocess_data, make_project_savepoint_obj, make_text_obj, make_audio_obj, create_text_to_audio
from django.db import transaction
from api.service import AiParkService

aipark_service = AiParkService()

class AiParkAPI(APIView):
    def post(self, request, *args, **kwargs):
        return create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return get_list(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
@transaction.atomic()
def create(request, *args, **kwargs):
    datas = request.data
    complete_preprocess = preprocess_data(datas["data"])
    project_id = make_project_savepoint_obj()
    make_text_obj(project_id,complete_preprocess)
    make_audio_obj(project_id)    
    create_text_to_audio(project_id)
    return JsonResponse({"result":"Success"}, status=status.HTTP_201_CREATED)


@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request, *args, **kwargs):
    project_id = kwargs.get("project_id")
    page = request.GET.get("page", 1)
    return JsonResponse(aipark_service.get_list(project_id,page), safe=False)