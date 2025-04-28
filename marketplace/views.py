# marketplace/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import MarketplaceListing
from .forms import ListingForm, PurchaseForm
from pokemons.models import Pokemon

@login_required
def listing_list(request):
    # Get active marketplace listings
    listings = MarketplaceListing.objects.filter(status='active').exclude(seller=request.user)

    # Handle search/filter
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    type_filter = request.GET.get('type', '')

    # Get all available Pokemon types for the dropdown
    all_types = [
        'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
        'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
        'dragon', 'dark', 'steel', 'fairy'
    ]
    # Convert to title case for display
    all_types_display = [(t, t.capitalize()) for t in all_types]

    if query:
        listings = listings.filter(
            Q(pokemon__nickname__icontains=query) |
            Q(pokemon__species__name__icontains=query) |
            Q(pokemon__name__icontains=query) |
            Q(description__icontains=query)
        )

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    if type_filter:
        # This is more complex since types are stored in JSONField
        # For simplicity, we'll filter by custom Pokemon type
        listings = listings.filter(
            Q(pokemon__type__icontains=type_filter) |  # For custom Pokemon
            Q(pokemon__species__types__contains=[type_filter])  # For regular Pokemon
        )

    # Get user's listings
    my_listings = MarketplaceListing.objects.filter(seller=request.user)

    return render(request, 'marketplace/list.html', {
        'listings': listings,
        'my_listings': my_listings,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'type_filter': type_filter,
        'all_types': all_types_display,  # Pass this to the template
    })

@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk)

    # Check if user can purchase (can't buy own listings)
    can_purchase = listing.status == 'active' and listing.seller != request.user

    # Check if user can cancel (can only cancel own listings)
    can_cancel = listing.status == 'active' and listing.seller == request.user

    # Create purchase form if needed
    purchase_form = None
    if can_purchase:
        purchase_form = PurchaseForm()

    return render(request, 'marketplace/detail.html', {
        'listing': listing,
        'can_purchase': can_purchase,
        'can_cancel': can_cancel,
        'purchase_form': purchase_form,
    })

@login_required
def create_listing(request):
    # Check if Pokemon ID was passed in the URL
    pokemon_id = request.GET.get('pokemon')
    initial_data = {}

    if pokemon_id:
        try:
            # Make sure the Pokemon exists and belongs to the user
            pokemon = Pokemon.objects.get(id=pokemon_id, trainer=request.user)
            initial_data['pokemon'] = pokemon
        except Pokemon.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.status = 'active'
            listing.save()

            messages.success(request, f"Your Pokemon has been listed in the marketplace for {listing.price} coins!")
            return redirect('marketplace:detail', pk=listing.pk)
    else:
        form = ListingForm(user=request.user, initial=initial_data)

    return render(request, 'marketplace/create.html', {'form': form})

@login_required
def purchase_listing(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk, status='active')

    # Check if user is trying to buy their own listing
    if listing.seller == request.user:
        messages.error(request, "You cannot purchase your own listing!")
        return redirect('marketplace:detail', pk=listing.pk)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Check if user has enough coins
            if request.user.currency < listing.price:
                messages.error(request, f"You don't have enough coins! You need {listing.price} coins, but you only have {request.user.currency}.")
                return redirect('marketplace:detail', pk=listing.pk)

            # Process the purchase
            success, message = listing.purchase(request.user)

            if success:
                messages.success(request, message)
                return redirect('pokemons:detail', pk=listing.pokemon.pk)
            else:
                messages.error(request, message)
                return redirect('marketplace:detail', pk=listing.pk)

    # If not POST or form invalid, redirect to listing detail
    return redirect('marketplace:detail', pk=listing.pk)

@login_required
def cancel_listing(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk, seller=request.user, status='active')

    listing.status = 'cancelled'
    listing.save()

    messages.success(request, "Your listing has been cancelled!")
    return redirect('marketplace:list')

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(MarketplaceListing, pk=pk, seller=request.user)

    # Only allow deletion if the listing is already cancelled or expired
    if listing.status != 'active':
        listing.delete()
        messages.success(request, "Listing has been permanently deleted!")
    else:
        messages.error(request, "You must cancel an active listing before deleting it.")

    return redirect('marketplace:list')