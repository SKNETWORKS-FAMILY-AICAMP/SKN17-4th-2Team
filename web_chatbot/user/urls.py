from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),                # 1. 시작 페이지
    path('login/', views.login_view, name='login'),     # 2. 로그인 페이지
    
    # 3. 회원가입
    # (1) 개인정보 약관 동의
    path('signup/', views.signup_step1_tos, name='signup_step1'),
    # # (2) 이메일 입력
    path('signup/email/', views.signup_step2_email, name='signup_step2'),
    # ⭐️ 2.1 (신규) "전송" 버튼이 호출할 API
    path('api/send_code/', views.api_send_code, name='api_send_code'),
    # ⭐️ 2.2 (신규) "확인" 버튼이 호출할 API
    path('api/verify_code/', views.api_verify_code, name='api_verify_code'),    
    # # (3) 비밀번호 설정
    path('signup/password/', views.signup_step3_password, name='signup_step3'),
]