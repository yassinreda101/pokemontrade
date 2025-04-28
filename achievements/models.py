# achievements/models.py

from django.db import models
from accounts.models import Trainer

class Achievement(models.Model):
    """
    Model for achievements that trainers can earn
    """
    CATEGORY_CHOICES = [
        ('collection', 'Collection'),
        ('battle', 'Battle'),
        ('trading', 'Trading'),
        ('marketplace', 'Marketplace'),
        ('special', 'Special'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.ImageField(upload_to='achievement_icons/', null=True, blank=True)
    experience_reward = models.IntegerField(default=100)
    currency_reward = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class TrainerAchievement(models.Model):
    """
    Model to track achievements earned by trainers
    """
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'achievement')

    def __str__(self):
        return f"{self.trainer.username} - {self.achievement.name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Grant rewards when achievement is first earned
        if is_new:
            # Grant XP
            self.trainer.increase_xp(self.achievement.experience_reward)

            # Grant currency
            if self.achievement.currency_reward > 0:
                self.trainer.currency += self.achievement.currency_reward
                self.trainer.save()

class Badge(models.Model):
    """
    Model for badges that trainers can earn (similar to gym badges)
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badge_icons/', null=True, blank=True)
    experience_reward = models.IntegerField(default=200)
    difficulty = models.IntegerField(default=1)  # 1-10 scale

    def __str__(self):
        return self.name

class TrainerBadge(models.Model):
    """
    Model to track badges earned by trainers
    """
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'badge')

    def __str__(self):
        return f"{self.trainer.username} - {self.badge.name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Grant rewards when badge is first earned
        if is_new:
            # Grant XP
            self.trainer.increase_xp(self.badge.experience_reward)
            self.trainer.save()