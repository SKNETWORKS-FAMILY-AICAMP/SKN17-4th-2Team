from django.db import models
from django.contrib.auth.models import User     # User 테이블은 Django에 이미 만들어져 있음

class Chat(models.Model):
    TYPE_CHOICES = [ ('youth', '청년'), ('newly1', '신혼1'), ('newly2', '신혼2')]           # chat type 선택지 정의
    user = models.ForeignKey(User, on_delete=models.CASCADE)                               # (FK)
    chat_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='youth')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title} (by {self.user.email})"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)    # (FK)
    content = models.TextField()
    sender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.sender}] {self.content[:30]}"   
