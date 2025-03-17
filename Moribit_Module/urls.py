# urls.py

from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='create_user'),
    path('login', views.LoginView.as_view(), name='login_user'),
    path('userdata', views.UserDetailView.as_view(), name='data_user'),
    path('UpdateUserData', views.UserDetailUpdate.as_view(), name='update_data_user'),
    path('code',views.Codeview.as_view(), name='code'),
    path('resetpassword', views.ChangePasswordView.as_view(), name='reset_password'),
    path('userlink', views.UserLinks.as_view(), name='user_links'),



    path('giftcheck', views.Giftcheckview.as_view(), name='gift_check'),
    path('webappgiftcod',views.webappgiftcodview.as_view(), name='webappgiftcod'),
    path('webappgiftcodcheck',views.WebAppGiftCodeCheck.as_view(), name='webappgiftcodcheck'),
    path('userdaily',views.userdailyview.as_view(), name='userdaily'),
    path('chat',views.chatbotview.as_view(), name='chat'),

    path('404', views.custom_404_view, name='custom_404'),

]

handler404 = 'Moribit_Module.views.custom_404_view'
