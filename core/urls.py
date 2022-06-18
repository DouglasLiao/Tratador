from django.urls import path

from .views import IndexView, AnimaisView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('animais/', AnimaisView.as_view(), name='animais')
]

