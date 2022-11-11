from api.models import Project
from api.serializers import TextModelSerializer
class AiParkService:
    def __init__(self):
        pass        

    def get_list(self, project_id, page):
        default= 10
        obj = Project.objects.get(id=project_id)
        text = obj.text_set.all()[int(page)*default-10:int(page)*10]
        serailizer = TextModelSerializer(instance=text, many=True)
        return serailizer.data