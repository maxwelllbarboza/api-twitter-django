from django.urls import path
from . import views

urlpatterns = [   
    path('register/', views.register_user, name= 'create_user'),  
    path('login/', views.login_user, name= 'login_user'),
    path('logout/', views.logout_user, name= 'logout_user'), 
    path('usuarios/', views.get_users, name= 'get_all_users'),
    path('user/', views.current_user, name= 'get_all_users'),    
    path('listarpost/', views.get_posts, name='get_posts'),
    path('criarpost/', views.create_post, name='create_post'),
    path('follow/', views.follow_user, name='follow_user'),
    path('unfollow/', views.unfollow_user, name='unfollow_user'),
]