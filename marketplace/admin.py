# marketplace/admin.py

from django.contrib import admin
from .models import MarketplaceListing

class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'seller', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('pokemon__nickname', 'pokemon__name', 'seller__username')

admin.site.register(MarketplaceListing, MarketplaceListingAdmin)