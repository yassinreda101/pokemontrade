# trades/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Trade, TradeItem
from .forms import TradeForm, TradeItemForm, TradeRespondForm
from pokemons.models import Pokemon

@login_required
def trade_list(request):
    # Get user's trades
    proposed_trades = Trade.objects.filter(proposer=request.user)
    received_trades = Trade.objects.filter(recipient=request.user)

    return render(request, 'trades/list.html', {
        'proposed_trades': proposed_trades,
        'received_trades': received_trades,
    })

@login_required
def trade_detail(request, pk):
    # Find the trade by primary key
    trade = get_object_or_404(Trade, pk=pk)

    # Make sure the user is involved in this trade
    if trade.proposer != request.user and trade.recipient != request.user:
        messages.error(request, "You are not authorized to view this trade.")
        return redirect('trades:list')

    # Get Pokemon involved in the trade
    proposer_items = TradeItem.objects.filter(trade=trade, trainer=trade.proposer)
    recipient_items = TradeItem.objects.filter(trade=trade, trainer=trade.recipient)

    # Determine what actions are available
    can_add_pokemon_proposer = trade.status == 'pending' and request.user == trade.proposer
    can_add_pokemon_recipient = trade.status == 'pending' and request.user == trade.recipient
    can_respond = trade.status == 'pending' and request.user == trade.recipient
    can_cancel = trade.status == 'pending' and request.user == trade.proposer

    # Create forms
    add_item_form = None
    respond_form = None

    if can_add_pokemon_proposer or can_add_pokemon_recipient:
        add_item_form = TradeItemForm(trainer=request.user)

    if can_respond:
        respond_form = TradeRespondForm()

    return render(request, 'trades/detail.html', {
        'trade': trade,
        'proposer_items': proposer_items,
        'recipient_items': recipient_items,
        'can_add_pokemon_proposer': can_add_pokemon_proposer,
        'can_add_pokemon_recipient': can_add_pokemon_recipient,
        'can_respond': can_respond,
        'can_cancel': can_cancel,
        'add_item_form': add_item_form,
        'respond_form': respond_form,
    })

@login_required
def create_trade(request):
    # Check if Pokemon ID was passed in the URL
    pokemon_id = request.GET.get('pokemon')
    initial_data = {}

    if request.method == 'POST':
        form = TradeForm(request.POST, user=request.user)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.proposer = request.user
            trade.status = 'pending'
            trade.save()

            # If a Pokemon was specified in the URL, add it to the trade
            if pokemon_id:
                try:
                    pokemon = Pokemon.objects.get(id=pokemon_id, trainer=request.user)
                    TradeItem.objects.create(
                        trade=trade,
                        trainer=request.user,
                        pokemon=pokemon
                    )
                except Pokemon.DoesNotExist:
                    pass

            messages.success(request, f"Trade offer created! Add Pokemon to your trade offer.")
            return redirect('trades:detail', pk=trade.pk)
    else:
        form = TradeForm(user=request.user)

    return render(request, 'trades/create.html', {'form': form})

# Fixed add_trade_item view
@login_required
def add_trade_item(request, trade_id):
    # First find trades where this user is involved
    trade_query = Trade.objects.filter(
        pk=trade_id,
        status='pending'
    ).filter(
        Q(proposer=request.user) | Q(recipient=request.user)
    )

    # Then get the trade or return 404
    trade = get_object_or_404(trade_query)

    if request.method == 'POST':
        form = TradeItemForm(request.POST, trainer=request.user)
        if form.is_valid():
            pokemon = form.cleaned_data['pokemon']

            # Check if this Pokemon is already in the trade
            if TradeItem.objects.filter(trade=trade, pokemon=pokemon).exists():
                messages.error(request, "This Pokemon is already included in the trade!")
            else:
                # Add Pokemon to trade
                TradeItem.objects.create(
                    trade=trade,
                    trainer=request.user,
                    pokemon=pokemon
                )
                messages.success(request, f"{pokemon.display_name} added to the trade!")

    return redirect('trades:detail', pk=trade_id)

@login_required
def remove_trade_item(request, item_id):
    # Get trade item and ensure user is the owner
    item = get_object_or_404(TradeItem, pk=item_id, trainer=request.user)
    trade = item.trade

    # Check if trade is still pending
    if trade.status != 'pending':
        messages.error(request, "This trade can no longer be modified!")
        return redirect('trades:detail', pk=trade.pk)

    # Remove the item
    pokemon_name = item.pokemon.display_name
    item.delete()

    messages.success(request, f"{pokemon_name} removed from the trade!")
    return redirect('trades:detail', pk=trade.pk)

@login_required
def respond_to_trade(request, pk):
    # Get trade and ensure user is the recipient
    trade = get_object_or_404(Trade, pk=pk, recipient=request.user, status='pending')

    if request.method == 'POST':
        form = TradeRespondForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']

            if action == 'accept':
                # Accept the trade
                success, message = trade.accept()
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, message)
            else:
                # Reject the trade
                success, message = trade.reject()
                messages.info(request, message)

    return redirect('trades:detail', pk=trade.pk)

@login_required
def cancel_trade(request, pk):
    # Get trade and ensure user is the proposer
    trade = get_object_or_404(Trade, pk=pk, proposer=request.user, status='pending')

    # Cancel the trade
    success, message = trade.cancel()
    messages.info(request, message)

    return redirect('trades:list')

@login_required
def trade_recommendations(request):
    """
    Show AI-powered trade recommendations for the current user
    """
    from .services import get_trade_recommendations

    # Get recommendations
    recommendations = get_trade_recommendations(request.user)

    return render(request, 'trades/recommendations.html', {
        'recommendations': recommendations,
    })