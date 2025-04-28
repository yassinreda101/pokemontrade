# trades/models.py

from django.db import models
from pokemons.models import Pokemon
from accounts.models import Trainer
from pokemon_trading_app.observers import Subject

class Trade(models.Model, Subject):
    """
    Model for Pokemon trades between trainers
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    proposer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='proposed_trades')
    recipient = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='received_trades')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        Subject.__init__(self)

    def __str__(self):
        return f"Trade #{self.id}: {self.proposer.username} → {self.recipient.username}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.notify(event_type='trade_proposed', trade=self)

    # Updated Trade model's accept method
    def accept(self):
        """
        Accept the trade and process the exchange
        """
        if self.status != 'pending':
            return False, "This trade can no longer be accepted"

        # Get all Pokemon involved in the trade
        proposer_pokemon = TradeItem.objects.filter(trade=self, trainer=self.proposer)
        recipient_pokemon = TradeItem.objects.filter(trade=self, trainer=self.recipient)

        # Check if both users have added Pokemon
        if not proposer_pokemon.exists():
            return False, "The proposer hasn't added any Pokémon to the trade yet"

        if not recipient_pokemon.exists():
            return False, "You need to add at least one Pokémon to the trade before accepting"

        # Exchange ownership
        for item in proposer_pokemon:
            item.pokemon.trainer = self.recipient
            item.pokemon.save()

        for item in recipient_pokemon:
            item.pokemon.trainer = self.proposer
            item.pokemon.save()

        # Update trade status
        self.status = 'accepted'
        self.save()

        # Notify observers
        self.notify(event_type='trade_accepted', trade=self)

        # Grant XP to both trainers
        self.proposer.increase_xp(50)
        self.recipient.increase_xp(50)

        # Check achievements and badges for both trainers
        from achievements.services import check_achievements
        check_achievements(self.proposer)
        check_achievements(self.recipient)

        return True, "Trade accepted and completed!"

    def reject(self):
        """
        Reject the trade
        """
        if self.status != 'pending':
            return False, "This trade can no longer be rejected"

        self.status = 'rejected'
        self.save()

        # Notify observers
        self.notify(event_type='trade_rejected', trade=self)

        return True, "Trade rejected"

    def cancel(self):
        """
        Cancel the trade (only proposer can cancel)
        """
        if self.status != 'pending':
            return False, "This trade can no longer be cancelled"

        self.status = 'cancelled'
        self.save()

        # Notify observers
        self.notify(event_type='trade_cancelled', trade=self)

        return True, "Trade cancelled"

class TradeItem(models.Model):
    """
    Model for Pokemon items included in a trade
    """
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='items')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('trade', 'pokemon')

    def __str__(self):
        return f"{self.pokemon.display_name} in Trade #{self.trade.id}"