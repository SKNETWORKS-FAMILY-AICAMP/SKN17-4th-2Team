from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from chat.models import Chat, Message
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
import json

# (임시) 챗봇 응답 함수. 나중에 이 함수를 실제 챗봇 RAG 또는 LLM API로 교체
def get_bot_response(user_message):
    # ==== 여기에다가 모델 api 추론 코드 작성 ====
    return f"이것은 '{user_message}'에 대한 임시 챗봇 응답입니다."


# 1. 채팅 메인
@login_required
def chat_main(request):
    chat_history = Chat.objects.filter(user=request.user).order_by('-created_at')   # 채팅로그 최신순으로 가져옴
    context = {
        'chat_history': chat_history,
        'is_logged_in': True, # @login_required 때문에 항상 True
        'user_email': request.user.email
    }
    return render(request, 'html/chat.html', context)

# 2. 새 채팅 버튼
@login_required
@require_POST   # POST 요청만 허용
def api_create_new_chat(request):
    try:
        new_chat = Chat.objects.create(user=request.user)   # 새 채팅방 생성
        
        initial_bot_message = "안녕하세요! 무엇을 도와드릴까요? (임시)"     # 챗봇 첫 인사말
        Message.objects.create(
            chat=new_chat,
            content=initial_bot_message,
            sender='bot'
        )
        
        return JsonResponse({
            'success': True,
            'new_chat_id': new_chat.id,
            'initial_message': {
                'content': initial_bot_message,
                'sender': 'bot'
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# 3. 채팅 로그 불러오기
@login_required
@require_GET    # GET 요청만 허용 (URL에 chat_id 포함) -> ????? 무슨 뜻인지 이해못함
def api_get_chat_history(request, chat_id):
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)   # chat_id로 DB에서 Chat 찾음
        
        # 해당 Chat의 모든 Message를 시간순으로 가져옴
        messages = Message.objects.filter(chat=chat).order_by('created_at').values(
            'content', 'sender'
        )
        message_list = list(messages)   
        
        return JsonResponse({'success': True, 'messages': message_list})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# 4. 이전 대화 계속 이어가기
@login_required
@require_POST
def api_send_message(request):
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        user_message_content = data.get('message')
        
        if not chat_id or not user_message_content:
            return JsonResponse({'success': False, 'error': '채팅방 ID 또는 메시지가 없습니다.'}, status=400)
        
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        
        # 사용자 메시지 DB에 저장
        Message.objects.create(
            chat=chat,
            content=user_message_content,
            sender='user'
        )
        
        # 챗봇 응답 생성 (임시 함수 호출)
        bot_response_content = get_bot_response(user_message_content)
        
        # 챗봇 응답 DB에 저장
        bot_msg = Message.objects.create(
            chat=chat,
            content=bot_response_content,
            sender='bot'
        )
        
        # 챗봇 응답 반환
        return JsonResponse({
            'success': True,
            'bot_message': {
                'content': bot_msg.content,
                'sender': bot_msg.sender
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)









# 여기서부터 참고
# ===========================================================================================

# def call_runpod_api(message, user_info):
#     try:
#         api_url = "https://x76r8kryd0u399-7004.proxy.runpod.net/chat"
#         payload = {
#             "message": message,
#             "user_info": user_info
#         }
#         res = requests.post(api_url, json=payload, timeout=120)
#         res.raise_for_status()
#         data = res.json()
#         return data.get("response", "⚠️ 응답이 없습니다.")
#     except Exception as e:
#         return f"❗ 오류 발생: {str(e)}"

