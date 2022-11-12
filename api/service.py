from api.models import Project, Text
from api.serializers import TextModelSerializer
from api.exceptions import NotFoundObject
from math import ceil

class AiParkService:
    def get_list(self, project_id, page):
        try:
            page_size = 10
            limit = page_size * int(page)
            offset = limit - page_size
            obj = Project.objects.get(id=project_id)
            cnt = obj.text_set.count()
            page_text = obj.text_set.all()[offset:limit]
            serailizer = TextModelSerializer(instance=page_text, many=True)
            page_count = ceil(cnt / page_size)
            context = [{
                "page": page,
                "page_count": page_count
            }]
            return serailizer.data, context
        except Project.DoesNotExist:
            raise NotFoundObject()
    
    def update(self, data, project_id, text_id, partial):
        try:
            instance = Text.objects.get(project_id=project_id, id=text_id)
            serializer = TextModelSerializer(instance, data=data, partial=partial)
            
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return serializer.data
        except Text.DoesNotExist:
            raise NotFoundObject()

    def perform_update(self, serializer):
        serializer.save()