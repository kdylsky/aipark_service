import re
from api.models import *

def preprocess_data(datas):
    phase1 = datas.strip()
    phase2 = re.split("[.?!]",phase1)
    result = [re.sub("[^\w|가-힣+?!.,\s]", "", i).strip() for i in phase2 if len(i)>0]
    return result

def make_project_savepoint_obj():
    project = Project.objects.create(
        project_title="프로젝트" #프로젝트/현재시간/유저이름
    )
    SavePoint.objects.create(
        project=project,
        savepoint=f"./savepoint/{project.id}{project.project_title}/"    
    )
    return project.id
    
def make_text_obj(project_id, complete_preprocess):
    for i in complete_preprocess:
        Text.objects.create(
            project=Project.objects.get(id=project_id),
            text=i
        )

def make_audio_obj(project_id):
    for k, j in enumerate(Text.objects.filter(project=Project.objects.get(id=project_id)).all(),1):
        Audio.objects.create(
            text=j,
            savepoint=SavePoint.objects.get(project=Project.objects.get(id=project_id)),
            index=k
        )