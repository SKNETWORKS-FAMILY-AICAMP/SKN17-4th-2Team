import string
import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

def index(request):
    return render(request, 'user/index.html')

def login_view(request):
    if request.method == 'POST':
        # --- 1. POST: 로그인 시도 ---
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1-1. 빈 값 검사
        if not email or not password:
            messages.error(request, '이메일과 비밀번호를 모두 입력해주세요.')
            return render(request, 'user/login.html')

        # 1-2. DB 인증 시도 (username 필드에 email 값을 사용)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # 1-3. 인증 성공
            login(request, user) # ⭐️ 세션 생성 (로그인)
            
            # ⭐️ 챗봇 메인 페이지로 리디렉션
            return redirect('chat:chat_main') 
        else:
            # 1-4. 인증 실패
            messages.error(request, '이메일 또는 비밀번호가 올바르지 않습니다.')
            return render(request, 'user/login.html')

    else:
        # --- 2. GET: 로그인 폼 보여주기 ---
        return render(request, 'user/login.html')

# 인증 코드 생성 함수
def generate_random_code(length=8):
    characters = string.ascii_letters
    return "".join(random.choices(characters, k=length))


def signup_step1_tos(request):
    if request.method == 'POST':
        # 1-1. ⭐️ name="tos_agreed"와 name="privacy_agreed"를 확인
        tos_agreed = request.POST.get('tos_agreed')
        privacy_agreed = request.POST.get('privacy_agreed')

        # 1-2. ⭐️ 둘 다 체크되었는지 확인
        if tos_agreed == 'on' and privacy_agreed == 'on':
            # 1-3. 세션에 '동의함' 기록
            request.session['agreed_to_terms'] = True 
            # 1-4. 다음 단계(이메일 입력)로 이동
            return redirect('user:signup_step2')
        else:
            # 1-5. (JS가 비활성화된 경우 등을 대비한) 백엔드 최종 방어
            messages.error(request, '필수 약관 2가지에 모두 동의하셔야 합니다.')
            return render(request, 'user/signin_01.html')
    else:
        # GET 요청: 약관 동의 폼 보여주기
        return render(request, 'user/signin_01.html')

# 2단계: 이메일 입력 (signin_02.html)
def signup_step2_email(request):
    # 2-0. 1단계 통과 확인
    if not request.session.get('agreed_to_terms'):
        return redirect('user:signup_step1')
    
    # ⭐️ POST 로직은 모두 api_send_code로 이동
    # ⭐️ GET 요청은 그냥 템플릿만 렌더링
    return render(request, 'user/signin_02.html')

from django.http import JsonResponse # ⭐️ 1. JSON 응답용
import json # ⭐️ 2. JSON 파싱용

def api_send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'error': '이메일이 필요합니다.'}, status=400)
            
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': '이미 가입된 이메일입니다.'}, status=400)

        verification_code = generate_random_code() # (이제 숫자 8자리)
        request.session['verification_email'] = email
        request.session['verification_code'] = verification_code
        
        message = render_to_string('user/activation_email.html', {'code': verification_code})
        try:
            send_mail(
                subject='[웹 챗봇] 회원가입 인증 코드입니다.',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'message': '인증 코드가 발송되었습니다.'})
        except Exception as e:
            return JsonResponse({'error': f'메일 발송 오류: {e}'}, status=500)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)


# ⭐️ 2.2 (신규) "확인" 버튼 API
def api_verify_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_code = data.get('code')
        correct_code = request.session.get('verification_code')
        
        if user_code == correct_code:
            request.session['email_verified'] = True
            if 'verification_code' in request.session:
                del request.session['verification_code'] 
            return JsonResponse({'verified': True}) # ⭐️ 성공!
        else:
            return JsonResponse({'verified': False, 'error': '코드가 일치하지 않습니다.'}, status=400)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)

# 3단계: 비밀번호 설정 (signin_03.html)
def signup_step3_password(request):
    # 3-0. ⭐️ 비정상 접근 방지: 2.5단계를 통과했는지 확인
    if not request.session.get('email_verified'):
        return redirect('user:signup_step2')

    if request.method == 'POST':
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            # ⭐️ 템플릿 이름: signin_03.html
            return render(request, 'user/signin_03.html')
        
        email = request.session.get('verification_email')
        if not email:
             return redirect('user:signup_step2') 

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.is_active = True 
            user.save()
            
            request.session.flush() # 가입 완료! 모든 세션 삭제
            login(request, user) # 자동 로그인
            
            return redirect('chat:chat_main') # 챗봇 메인으로
            
        except Exception as e:
            messages.error(request, f'계정 생성 오류: {e}')
            # ⭐️ 템플릿 이름: signin_03.html
            return render(request, 'user/signin_03.html')

    # GET 요청: 비밀번호 생성 폼 보여주기
    # ⭐️ 템플릿 이름: signin_03.html
    return render(request, 'user/signin_03.html')