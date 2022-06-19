from django.urls import path

from .views import IndexView, AnimaisView, AnimaisListApiView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('animais/', AnimaisView.as_view(), name='animais'),
    path('api/', AnimaisListApiView.as_view()),
]

