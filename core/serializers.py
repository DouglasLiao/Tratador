from rest_framework import serializers
from .models import Animais

class AnimaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animais
        fields = ['id', 'comeu', 'bebeu', 'saiu', 'peso', 'saude']