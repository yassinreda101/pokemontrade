# chat/models.py

from django.db import models
from accounts.models import Trainer

class ChatRoom(models.Model):
    """
    Model for chat rooms between trainers
    """
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(Trainer, related_name='chat_rooms')
    is_trade_room = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    """
    Model for individual chat messages
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"