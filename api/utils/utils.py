import os
import re
from gtts import gTTS
from api.models import *
from datetime import datetime

def preprocess_data(datas):
    phase1 = datas.strip()
    phase2 = re.compile(r'([^\.!?]*[\.!?])', re.M)
    phase3 = phase2.findall(phase1)
    result = [re.sub("[^\w|가-힣+?!.,\s]", "", i).strip() for i in phase3 if len(i)>0]
    return result

def make_project_obj():
    project = Project.objects.create(
        project_title="프로젝트", #프로젝트/현재시간/유저이름
        savedpoint=""
    )
    project.savedpoint=f"../savepoint/{project.project_title}{project.id}번"
    project.save()
    return project.id
    
def make_text_obj(project_id, complete_preprocess):
    for i,j in enumerate(complete_preprocess,1):
        Text.objects.create(
            project=Project.objects.get(id=project_id),
            text=j,
            index=i
        )

def create_text_to_audio(project_id):
    try:
        text_list = Text.objects.filter(project__id=project_id).order_by("index")
        path=text_list[0].project.savedpoint+datetime.now().strftime('%Y-%m-%d-%H시%M분/')
        os.makedirs(path)
        for audio in text_list:
            real_audio = gTTS(text=audio.text, lang="ko", slow=audio.speed)
            real_audio.save(path+f"{audio.index}.mp3")
    except:
        return False
    else:
        return True    