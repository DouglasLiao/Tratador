import django_tables2 as tables
from .models import Animais

class AnimaisTable(tables.Table):
    class Meta:
        model = Animais
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","comeu", "bebeu", "saiu", "peso", "saude")