
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('messages', views.messages, name='messages'),
    path('profile', views.profile, name='profile'),
    #path('login/', login_view, name='login'),
    path('logout', views.logout, name='logout'),
]