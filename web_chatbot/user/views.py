import string
import random
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# 인증 코드 생성 함수
def generate_random_code(length=8):
    characters = string.ascii_letters   # 영문 8자리
    return "".join(random.choices(characters, k=length))

# ============================================================================

# 1. intro.html (시작)
def index(request):
    return render(request, 'html/main.html')

# ============================================================================

# 2. login.html (로그인)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, '이메일과 비밀번호를 모두 입력해주세요.')
            return render(request, 'html/login.html')

        # 로그인 시도
        user = authenticate(request, username=email, password=password)

        # 로그인 O -> 채팅 페이지
        if user is not None:    
            login(request, user)
            return redirect('chat:chat_main')
        # 로그인 X -> 계속 로그인 페이지
        else:
            messages.error(request, '이메일 또는 비밀번호가 올바르지 않습니다.')
            return render(request, 'html/login.html')
    else:
        return render(request, 'html/login.html')
    
# ============================================================================

# 3. sign.html (회원가입)
def sign_view(request):
    return render(request, 'html/sign.html')

# 3.1 인증 코드 전송 버튼 API
def api_send_sign_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'error': '이메일이 필요합니다.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': '이미 가입된 이메일입니다.'}, status=400)

        code = generate_random_code(8)                                          # 인증코드 생성
        message = render_to_string('html/signup_email.html', {'code': code})    # 전송할 email
        # email 전송
        try:
            send_mail(
                subject='[RoomMate] 회원가입 인증 코드입니다.',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            request.session['signup_email'] = email
            request.session['signup_code'] = code
            return JsonResponse({'message': '인증 코드가 발송되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': f'메일 발송 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 3.2 인증 코드 확인 버튼 API
def api_verify_sign_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_code = data.get('code')
        correct_code = request.session.get('signup_code')
        
        # 인증코드 일치하는지 확인
        if user_code == correct_code:
            request.session['signup_verified'] = True
            return JsonResponse({'verified': True})
        else:
            return JsonResponse({'verified': False, 'error': '코드가 일치하지 않습니다.'}, status=400)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 3.3 인증 후 비밀번호 설정 API
def api_create_user(request):
    if request.method == 'POST':
        # 이메일 인증 안하면
        if not request.session.get('signup_verified'):
            return JsonResponse({'error': '이메일 인증이 필요합니다.'}, status=403)

        email = request.session.get('signup_email')
        data = json.loads(request.body)
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': '세션이 만료되었거나 비밀번호가 없습니다.'}, status=400)
        try:
            # user 저장
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)    # 자동 로그인 시킴
            
            # 세션 정리
            request.session.pop('signup_email', None)
            request.session.pop('signup_code', None)
            request.session.pop('signup_verified', None)
            
            return JsonResponse({'created': True, 'redirect_url': '/chat/'})    # 회원가입 성공하면 로그인 페이지로 이동 ??? 왜냐면 로그인 유지된 채이기 때문
        except Exception as e:
            return JsonResponse({'error': f'계정 생성 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# ============================================================================

# 4. 비밀번호 재설정
def password_reset_view(request):
    return render(request, 'html/password_reset.html')

# 4.1 인증 코드 전송 버튼 API
def api_send_reset_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'error': '이메일을 입력해주세요.'}, status=400) 
        try:
            user = User.objects.get(email=email)
        # (보안 조치) 어떤 이메일이 가입되었는지 추측할 수 없게
        except User.DoesNotExist:   
            return JsonResponse({'message': '인증 코드가 발송되었습니다.'})

        code = generate_random_code(8)                                                  # 인증코드 생성
        message = render_to_string('html/password_reset_email.html', {'code': code})    # 전송할 email
        # email 전송
        try:
            send_mail(
                subject='[RoomMate] 비밀번호 재설정 인증 코드입니다.',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            request.session['reset_code'] = code
            return JsonResponse({'message': '인증 코드가 발송되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': f'메일 발송 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 4.2 인증 코드 확인 버튼 API
def api_verify_reset_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_code = data.get('code')
        correct_code = request.session.get('reset_code')
        
        # 인증코드 일치하는지 확인
        if user_code == correct_code:
            request.session['reset_verified'] = True 
            return JsonResponse({'verified': True})
        else:
            return JsonResponse({'verified': False, 'error': '코드가 일치하지 않습니다.'}, status=400)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 4.3 인증 후 새 비밀번호 설정 API
def api_set_reset_password(request):
    if request.method == 'POST':
        # 이메일 인증 안하면
        if not request.session.get('reset_verified'):
            return JsonResponse({'error': '이메일 인증이 필요합니다.'}, status=403)

        email = request.session.get('reset_email')
        data = json.loads(request.body)
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not email:
            return JsonResponse({'error': '세션이 만료되었습니다. 1단계부터 다시 시도하세요.'}, status=400)
        if not new_password or not confirm_password:
            return JsonResponse({'error': '새 비밀번호를 입력해주세요.'}, status=400)
        if new_password != confirm_password:
            return JsonResponse({'error': '새 비밀번호가 일치하지 않습니다.'}, status=400)
        try:
            # 새 비밀번호 저장
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # 세션 정리
            request.session.pop('reset_email', None)
            request.session.pop('reset_code', None)
            request.session.pop('reset_verified', None)
            
            return JsonResponse({'changed': True, 'redirect_url': '/login/'})   # 비번 재설정 성공하면 로그인 페이지로 이동
        except User.DoesNotExist:
             return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'비밀번호 변경 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# ============================================================================

# 5. password_modify (비밀번호 수정)
@login_required
def password_modify_view(request):
    return render(request, 'html/password_modify.html')

# 5.1 인증 코드 전송 버튼 API
@login_required
def api_send_modify_code(request):
    if request.method == 'POST':
        user = request.user
        code = generate_random_code(8)                                                  # 인증코드 생성
        message = render_to_string('html/password_modify_email.html', {'code': code})   # 전송할 email
        # email 전송
        try:
            send_mail(
                subject='[RoomMate] 비밀번호 수정 인증 코드입니다.',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            request.session['modify_code'] = code
            return JsonResponse({'message': '인증 코드가 발송되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': f'메일 발송 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 5.2 인증 코드 확인 버튼 API
@login_required
def api_verify_modify_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_code = data.get('code')
        correct_code = request.session.get('modify_code')
        
        # 인증코드 일치하는지 확인
        if user_code == correct_code:
            request.session['modify_verified'] = True 
            return JsonResponse({'verified': True})
        else:
            return JsonResponse({'verified': False, 'error': '코드가 일치하지 않습니다.'}, status=400)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 5.3 인증 후 새 비밀번호 수정 API
@login_required
def api_set_new_password(request):
    if request.method == 'POST':
        # 이메일 인증 안하면
        if not request.session.get('modify_verified'):
            return JsonResponse({'error': '이메일 인증이 필요합니다.'}, status=403)

        data = json.loads(request.body)
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not new_password or not confirm_password:
            return JsonResponse({'error': '새 비밀번호를 입력해주세요.'}, status=400)
        if new_password != confirm_password:
            return JsonResponse({'error': '새 비밀번호가 일치하지 않습니다.'}, status=400)
        try:
            # 수정된 비밀번호 저장
            user = request.user
            user.set_password(new_password)
            user.save()
            
            update_session_auth_hash(request, user)     # 비밀번호 변경 후 로그아웃 방지 기능
            
            # 세션 정리
            request.session.pop('modify_code', None)
            request.session.pop('modify_verified', None)
            
            # 비번 수정 성공하면 로그인 상태로 채팅 페이지로 이동 ????
            return JsonResponse({'changed': True, 'redirect_url': '/chat/'})    
        except Exception as e:
            return JsonResponse({'error': f'비밀번호 변경 오류: {e}'}, status=500)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)