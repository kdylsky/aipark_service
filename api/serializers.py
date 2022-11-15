from rest_framework import serializers
from api.models import Text

class ProjectSchema(serializers.Serializer):
    """ project 생성 요청 파마리터 """
    project_title = serializers.CharField(max_length=50)
    data = serializers.CharField(max_length=None)


class AddTextSchema(serializers.Serializer):
    """ 이미 존재하는 프로젝트에 텍스트 추가 요청 파라미터"""
    data = serializers.CharField(max_length=None)


class TextModelSerializer(serializers.ModelSerializer):
    """ partial update를 위한 serializer"""
    class Meta:
        model = Text
        fields = "__all__"
