from django.urls import path
from django.conf.urls import include
from django.contrib import admin

from .views import IndexView, AnimaisView, AnimaisListApiView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('animais/', AnimaisView.as_view(), name='animais'),
    path('api/', AnimaisListApiView.as_view()),
    path('student/',include('Student.urls',namespace='Student')),
    path('admin2/', admin.site.urls),
]

