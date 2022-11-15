from api.models import Project, Text
from api.serializers import TextModelSerializer
from api.exceptions import NotFoundObject
from math import ceil
from api.utils.utils import preprocess_data, make_project_obj, make_text_obj,  create_text_to_audio
from django.db import transaction


class AiParkService:
    @transaction.atomic()
    def create(self, user: object, datas: dict)-> bool:
        complete_preprocess = preprocess_data(datas["data"])
        project_id = make_project_obj(user, datas["project_title"])
        make_text_obj(user, project_id, complete_preprocess)
        result = create_text_to_audio(user, project_id) 
        return result

    def get_list(self, user: object, project_id: int, page: str)-> list:
        try:
            page_size = 10
            limit = page_size * int(page)
            offset = limit - page_size
            obj = Project.objects.get(id=project_id, user=user)
            cnt = obj.text_set.count()
            page_text = obj.text_set.all().order_by("index")[offset:limit]
            serailizer = TextModelSerializer(instance=page_text, many=True)
            page_count = ceil(cnt / page_size)
            context = [{
                "page": page,
                "page_count": page_count
            }]
            return serailizer.data, context
        except Project.DoesNotExist:
            raise NotFoundObject()
    
    def update(self, user: object, data: dict, project_id: int, index:int, partial: bool)-> dict:
        try:
            instance = Text.objects.get(project_id=project_id, index=index, project__user=user)
            serializer = TextModelSerializer(instance, data=data, partial=partial) 
            serializer.is_valid(raise_exception=True)
            self._perform_update(serializer)
            create_text_to_audio(user, project_id)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return serializer.data
        except Text.DoesNotExist:
            raise NotFoundObject()

    def _perform_update(self, serializer):
        serializer.save()

    def delete(self, user: object, project_id: int)-> dict:
        try:
            instance = Project.objects.get(id=project_id, user=user)
            return instance.delete()
        except Project.DoesNotExist:
            raise NotFoundObject()

    def add(self, user: object, project_id: int, datas: dict, index: int)-> bool:    
        if index == None:
            index = Text.objects.filter(project_id=project_id, project__user=user).count() + 1 
        complete_preprocess = preprocess_data(datas["data"])
        cnt = len(complete_preprocess)        
        texts = Text.objects.filter(project_id=project_id, index__gte=index, project__user=user)
        for text in texts:
            text.index+=cnt
            text.save()
        make_text_obj(user, project_id, complete_preprocess, int(index))
        result = create_text_to_audio(user, project_id) 
        return result