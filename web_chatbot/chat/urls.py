from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # 1. 채팅 메인 페이지
    path('', views.chat_main, name='chat_main'),

    # 2. 새 채팅 생성 API
    path('api/create_chat/', views.api_create_new_chat, name='api_create_new_chat'),

    # 3. 채팅 로그 불러오기 API
    path('api/history/<int:chat_id>/', views.api_get_chat_history, name='api_get_chat_history'),

    # 4. 메시지 전송
    path('api/send_message/', views.api_send_message, name='api_send_message'),
]