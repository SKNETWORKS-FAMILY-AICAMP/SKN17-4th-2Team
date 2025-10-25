from django.shortcuts import render
from django.contrib.auth.decorators import login_required





# 로그인 상태에서 main -> chat 잘 넘어가는지 확인 용도로 임시로 만듦 (수정해도 됩니다)
@login_required
def chat_main(request):
    return render(request, 'html/chat.html')