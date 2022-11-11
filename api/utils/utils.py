import os
import re
from gtts import gTTS
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
        savepoint=f"../savepoint/{project.project_title}{project.id}/"    
    )
    return project.id
    
def make_text_obj(project_id, complete_preprocess):
    for i,j in enumerate(complete_preprocess,1):
        Text.objects.create(
            project=Project.objects.get(id=project_id),
            text=j,
            index=i
        )

def make_audio_obj(project_id):
    for j in Text.objects.filter(project=Project.objects.get(id=project_id)):
        Audio.objects.create(
            text=j,
            savepoint=SavePoint.objects.get(project=Project.objects.get(id=project_id))
        )

def create_text_to_audio(project_id):
    audio_list = Audio.objects.filter(text__project__id=project_id)
    path=audio_list[0].savepoint.savepoint
    os.makedirs(path)
    for audio in audio_list:
        real_audio = gTTS(text=audio.text.text, lang="ko", slow=audio.speed)
        real_audio.save(path+f"{audio.id}.mp3")
