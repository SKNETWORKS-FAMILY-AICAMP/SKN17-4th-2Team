from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # 기본 view
    # path('', views.index, name='index'),

    
    # 로그인 상태에서 main -> chat 잘 넘어가는지 확인 용도로 임시로 만듦 (수정해도 됩니다)
    path('', views.chat_main, name='chat_main'),
]