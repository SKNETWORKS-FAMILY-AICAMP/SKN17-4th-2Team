from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 1. intro.html (시작 페이지)
    path('', views.index, name='index'),

    # 2. login.html (로그인)
    path('login/', views.login_view, name='login'),
    
    # --- 3. sign.html (회원가입) ---
    path('sign/', views.sign_view, name='sign'),
    path('api/send_sign_code/', views.api_send_sign_code, name='api_send_sign_code'),
    path('api/verify_sign_code/', views.api_verify_sign_code, name='api_verify_sign_code'),
    path('api/create_user/', views.api_create_user, name='api_create_user'),

    # --- 4. password_rest.html (비밀번호 재설정) ---
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('api/send_reset_code/', views.api_send_reset_code, name='api_send_reset_code'),
    path('api/verify_reset_code/', views.api_verify_reset_code, name='api_verify_reset_code'),
    path('api/set_reset_password/', views.api_set_reset_password, name='api_set_reset_password'),
    
    # --- 5. password_modify.html (비밀번호 변경, @login_required 필요) ---
    path('password_modify/', views.password_modify_view, name='password_modify'),
    path('api/send_modify_code/', views.api_send_modify_code, name='api_send_modify_code'),
    path('api/verify_modify_code/', views.api_verify_modify_code, name='api_verify_modify_code'),
    path('api/set_new_password/', views.api_set_new_password, name='api_set_new_password'),

    # 6. 로그아웃 경로
    path('logout/', views.logout_view, name='logout'),

    # 7. 회원 탈퇴
    path('withdraw/', views.api_withdraw_user, name = 'api_withdraw_user')
]