# achievements/admin.py

from django.contrib import admin
from .models import Achievement, TrainerAchievement, Badge, TrainerBadge

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'experience_reward', 'currency_reward')
    list_filter = ('category',)
    search_fields = ('name', 'description')

class TrainerAchievementAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'achievement', 'earned_at')
    list_filter = ('achievement__category',)
    search_fields = ('trainer__username', 'achievement__name')

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'experience_reward')
    list_filter = ('difficulty',)
    search_fields = ('name', 'description')

class TrainerBadgeAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'badge', 'earned_at')
    search_fields = ('trainer__username', 'badge__name')

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(TrainerAchievement, TrainerAchievementAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(TrainerBadge, TrainerBadgeAdmin)