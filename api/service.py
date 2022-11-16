from math               import ceil

from django.db          import transaction

from api.models         import Project, Text
from api.serializers    import TextModelSerializer
from api.exceptions     import NotFoundObject
from api.utils.utils    import preprocess_data, make_project_obj, make_text_obj, create_text_to_audio

class AiParkService:
    @transaction.atomic()
    def create(self, user: object, params: dict)-> bool:
        """
        프로젝트와 오디오 생성 함수(총 4단계)
        
        phase1단계: 전처리 단계 
        phase2단계: 프로젝트 객체만들기
        phase3단계: 텍스트 객체만들기
        phase4단계: 텍스트를 오디오로 만들기
        """
        complete_preprocess = preprocess_data(params["data"])
        project_id          = make_project_obj(user, params["project_title"])
        make_text_obj(user, project_id, complete_preprocess)
        created_audio       = create_text_to_audio(user, project_id) 
        return created_audio

    def get_list(self, user: object, project_id: int, page: str)-> list:
        """
        프로젝트의 텍스트를 10개 단위로 가지고 온다.
        """
        try:
            page_size   = 10
            page_limit  = page_size * int(page)
            offset      = page_limit - page_size
            project_obj = Project.objects.prefetch_related("text_set").get(id=project_id, user=user)
            text_cnt    = project_obj.text_set.count()
            page_text   = project_obj.text_set.all().order_by("index")[offset:page_limit]
            serailizer  = TextModelSerializer(instance=page_text, many=True)
            page_count  = ceil(text_cnt / page_size)
            context = [{
                "page": page,
                "page_count": page_count
            }]
            return context, serailizer.data
        except Project.DoesNotExist:
            raise NotFoundObject()
    
    def add_forward(self, user: object, project_id: int, index: int, params: dict)-> bool:    
        """
        사용자로 부터 삽입될 위치의 index를 받는다.
        만약 index == None이라면 text의 개수에 +1 한 위치부터 새로운 텍스트를 추가한다.
        그렇지 않다면, 해당 인덱스를 기준으로 뒤에 있는 모든 텍스트의 인덱스를, 새로 삽입될 텍스트의 개수 만큼 뒤로 미룬다.
        """
        try:
            if index == None:
                index = Text.objects.select_related("project", "project__user").filter(project_id=project_id, project__user=user).count() + 1 
            complete_preprocess = preprocess_data(params["data"])
            new_text_cnt        = len(complete_preprocess)        
            original_texts      = Text.objects.select_related("project", "project__user").filter(project_id=project_id, index__gte=index, project__user=user)
            for text in original_texts:
                text.index+=new_text_cnt
                text.save()
            make_text_obj(user, project_id, complete_preprocess, int(index))
            created_audio = create_text_to_audio(user, project_id) 
            return created_audio
        except Text.DoesNotExist:
            raise NotFoundObject()
    
    def delete(self, user: object, project_id: int)-> dict:
        try:
            instance = Project.objects.get(id=project_id, user=user)
            return instance.delete()
        except Project.DoesNotExist:
            raise NotFoundObject()

    def update(self, user: object, data: dict, project_id: int, index:int, partial: bool)-> dict:
        try:
            instance    = Text.objects.select_related("project", "project__user").get(project_id=project_id, index=index, project__user=user)
            serializer  = TextModelSerializer(instance, data=data, partial=partial) 
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
    
    def send_audio_file(self, user: object, project_id: int, index: int):
        save_point = Project.objects.get(user=user, id=project_id).savedpoint
        mp3_file   = open(f"{save_point}{index}.mp3", "rb")
        return mp3_file