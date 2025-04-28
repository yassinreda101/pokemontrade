# api/models.py

from django.db import models
from accounts.models import Trainer

class APILog(models.Model):
    """
    Model to track API usage
    """
    API_CHOICES = [
        ('pokeapi', 'PokeAPI'),
        ('pokemontcg', 'Pokemon TCG API'),
        ('openai', 'OpenAI API'),
    ]

    api_name = models.CharField(max_length=20, choices=API_CHOICES)
    endpoint = models.CharField(max_length=255)
    request_data = models.JSONField(null=True, blank=True)
    response_status = models.IntegerField()
    response_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.api_name} - {self.endpoint} - {self.timestamp}"