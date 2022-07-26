from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from django.conf import settings
from Student import views

from core.views import ReadListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('student', views.add_student, name='add_student'),
    path('student_manage', views.student_manage, name='student_manage'),
    path('student_edit/<int:pk>', views.student_edit, name='student_edit'),
    path('delete_student/<int:pk>', views.delete_student, name='delete_student'),
    path('show_graph', views.show_graph, name='show_graph'),
    path('read', ReadListView.as_view(), name='reader'),
    path('fetch_sensor_values_ajax', views.fetch_sensor_values_ajax, name='fetch_sensor_values_ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
