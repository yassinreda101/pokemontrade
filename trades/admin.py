# trades/admin.py

from django.contrib import admin
from .models import Trade, TradeItem

class TradeItemInline(admin.TabularInline):
    model = TradeItem
    extra = 1

class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposer', 'recipient', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('proposer__username', 'recipient__username')
    inlines = [TradeItemInline]

admin.site.register(Trade, TradeAdmin)