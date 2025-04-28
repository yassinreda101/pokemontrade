# marketplace/models.py

from django.db import models
from pokemons.models import Pokemon
from accounts.models import Trainer
from pokemon_trading_app.observers import Subject

class MarketplaceListing(models.Model, Subject):
    """
    Model for Pokemon listings in the marketplace
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ]

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    seller = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='listings')
    price = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        Subject.__init__(self)

    def __str__(self):
        return f"{self.pokemon.display_name} - {self.price} coins"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.notify(event_type='marketplace_listing', listing=self)

    def purchase(self, buyer):
        """
        Process the purchase of this listing
        """
        if self.status != 'active':
            return False, "This Pokemon is no longer available for purchase"

        if buyer.currency < self.price:
            return False, "You don't have enough coins"

        # Update buyer and seller currencies
        buyer.currency -= self.price
        self.seller.currency += self.price

        # Update Pokemon owner
        self.pokemon.trainer = buyer

        # Update listing status
        self.status = 'sold'

        # Save all changes
        buyer.save()
        self.seller.save()
        self.pokemon.save()
        self.save()

        # Notify observers
        self.notify(event_type='marketplace_sale', listing=self, buyer=buyer)

        # Check achievements and badges for both buyer and seller
        from achievements.services import check_achievements
        check_achievements(buyer)
        check_achievements(self.seller)

        return True, "Purchase successful!"