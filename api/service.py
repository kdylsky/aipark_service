from api.models import Project, Text
from api.serializers import TextModelSerializer
from api.exceptions import NotFoundObject
from math import ceil
from api.utils.utils import preprocess_data, make_project_obj, make_text_obj,  create_text_to_audio
from django.db import transaction


class AiParkService:
    @transaction.atomic()
    def create(self, datas):
        complete_preprocess = preprocess_data(datas["data"])
        project_id = make_project_obj()
        make_text_obj(project_id,complete_preprocess)
        result = create_text_to_audio(project_id) 
        return result

    def get_list(self, project_id, page):
        try:
            page_size = 10
            limit = page_size * int(page)
            offset = limit - page_size
            obj = Project.objects.get(id=project_id)
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
    
    def update(self, data, project_id, index, partial):
        try:
            instance = Text.objects.get(project_id=project_id, index=index)
            serializer = TextModelSerializer(instance, data=data, partial=partial) 
            serializer.is_valid(raise_exception=True)
            self._perform_update(serializer)
            create_text_to_audio(project_id)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return serializer.data
        except Text.DoesNotExist:
            raise NotFoundObject()

    def _perform_update(self, serializer):
        serializer.save()

    def delete(self, project_id):
        try:
            instance = Project.objects.get(id=project_id)
            return instance.delete()
        except Project.DoesNotExist:
            raise NotFoundObject()

    def add_create(self, project_id, datas, index):    
        if index == None:
            index = Text.objects.filter(project_id=project_id).count() + 1 
        complete_preprocess = preprocess_data(datas["data"])
        cnt = len(complete_preprocess)        
        texts = Text.objects.filter(project_id=project_id, index__gte=index)
        for text in texts:
            text.index+=cnt
            text.save()
        make_text_obj(project_id, complete_preprocess, int(index))
        result = create_text_to_audio(project_id) 
        return result