from django.urls import path

from acrofestival.content import views

app_name = 'content'

urlpatterns = [
    path('', views.content_editor_list, name='editor_list'),
    path('<str:festival>/', views.content_editor_edit, name='editor_edit'),
]
