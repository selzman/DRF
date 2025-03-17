from django.urls import path
from . import views



urlpatterns = [
    path('news', views.NewsView.as_view(), name='news_view'),
    path('confing', views.AppConfingView.as_view(), name='confing_view'),
    path('Dailybonus', views.DailybonusClaimView.as_view(), name='Daily_bonus_view'),
    path('tasks', views.tasksview.as_view(), name='tasks'),
    path('errors', views.adminalertview.as_view(), name='adminalertview'),
]