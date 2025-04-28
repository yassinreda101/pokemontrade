# api/admin.py

from django.contrib import admin
from .models import APILog

class APILogAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'endpoint', 'response_status', 'timestamp', 'user')
    list_filter = ('api_name', 'response_status')
    search_fields = ('endpoint', 'user__username')
    readonly_fields = ('api_name', 'endpoint', 'request_data', 'response_status', 'response_data', 'timestamp', 'user')

admin.site.register(APILog, APILogAdmin)