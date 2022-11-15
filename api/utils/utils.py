import os
import re
import shutil
from gtts import gTTS
from api.models import Text, Project

def preprocess_data(datas: str)-> list:
    """전처리 과정"""
    phase1 = datas.strip()
    phase2 = re.compile(r'([^\.!?]*[\.!?])', re.M)
    phase3 = phase2.findall(phase1)
    result = [re.sub("[^\w|가-힣+?!.,\s]", "", i).strip() for i in phase3 if len(i)>0]
    return result

def make_project_obj(user: object, project_title: str)-> int:
    """프로젝트 객체 만들기"""
    project = Project.objects.create(
        user = user,
        project_title=f"{project_title}_{user.id}user",
        savedpoint=""
    )
    project.savedpoint=f"../savepoint/{project.project_title}{project.id}번/"
    project.save()
    return project.id
    
def make_text_obj(user: object, project_id: int, complete_preprocess: list, cnt: int = 1)-> None:
    """텍스트 객체 만들기"""
    for i,j in enumerate(complete_preprocess, cnt):
        Text.objects.create(
            project=Project.objects.get(id=project_id, user=user),
            text=j,
            index=i
        )

def create_text_to_audio(user: object, project_id: int)-> bool:
    """텍스트 객체로 오디오파일 만들기"""
    try:
        text_list = Text.objects.filter(project__id=project_id, project__user=user).order_by("index")
        path = text_list[0].project.savedpoint
        if os.path.exists(path):
             shutil.rmtree(path)
        os.makedirs(path)
        for audio in text_list:
            real_audio = gTTS(text=audio.text, lang="ko", slow=audio.speed)
            real_audio.save(path+f"{audio.index}.mp3")
    except:
        return False
    else:
        return True    