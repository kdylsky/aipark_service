from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.service import AiParkService
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from decorators.auth_handler import login_decorator


aipark_service = AiParkService()

class AiParkView(APIView):
    def post(self, request, *args, **kwargs):
        return create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return get_list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return delete_project(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return create_text(request, *args, **kwargs)

class TextUpdateView(GenericAPIView, UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        return partial_update(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def create(request, *args, **kwargs):
    user = request.user
    datas = request.data
    return JsonResponse(aipark_service.create(user, datas), status=status.HTTP_201_CREATED, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def get_list(request, *args, **kwargs):
    user = request.user
    project_id = kwargs.get("project_id")
    page = request.GET.get("page", 1)
    serailizer, context = aipark_service.get_list(user,project_id, page)
    return JsonResponse({"page":context, "data": serailizer }, status=status.HTTP_200_OK, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def partial_update(request, *args, **kwargs):
    user = request.user
    data = request.data
    project_id = kwargs["project_id"]
    index= kwargs["index"]
    kwargs['partial'] = True
    partial = kwargs.pop('partial', False)
    return JsonResponse(aipark_service.update(user, data, project_id, index, partial), status=status.HTTP_200_OK)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def delete_project(request, *args, **kwargs):
    user = request.user
    project_id = kwargs["project_id"]
    return JsonResponse(aipark_service.delete(user, project_id), status=status.HTTP_204_NO_CONTENT, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def create_text(request, *args, **kwargs):
    user = request.user
    project_id = kwargs["project_id"]
    index = request.GET.get("index", None)
    datas = request.data
    return JsonResponse(aipark_service.add_create(user, project_id, datas, index), safe=False)

