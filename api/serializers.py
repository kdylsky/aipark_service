from rest_framework import serializers
from api.models import Text

class TextModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"
