# chat/admin.py

from django.contrib import admin
from .models import ChatRoom, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_trade_room', 'created_at')
    list_filter = ('is_trade_room',)
    search_fields = ('name',)
    inlines = [ChatMessageInline]

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'content', 'timestamp')
    list_filter = ('room__is_trade_room',)
    search_fields = ('sender__username', 'content', 'room__name')

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)