
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('profile', views.profile, name='profile'),
    path('create', views.register_user, name='create'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    #path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
