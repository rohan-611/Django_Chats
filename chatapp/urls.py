from . import views
from django.urls import path

app_name = 'chatapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
