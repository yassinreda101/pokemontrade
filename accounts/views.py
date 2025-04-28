# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TrainerRegistrationForm, TrainerLoginForm, TrainerProfileForm
from pokemon_trading_app.factories import StarterPokemonFactory

# accounts/views.py (updated register_view function)

def register_view(request):
    if request.method == 'POST':
        form = TrainerRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            trainer = form.save()

            # Give starter Pokemon
            factory = StarterPokemonFactory()
            starter_pokemon = factory.create_pokemon(trainer)

            # Check achievements and badges for new trainer
            from achievements.services import check_achievements
            check_achievements(trainer)

            # Log in the user - specify the backend
            login(request, trainer, backend='accounts.backends.EmailOrUsernameModelBackend')

            messages.success(request, f'Welcome, {trainer.username}! Your account has been created and you have received your starter Pokémon!')
            return redirect('home')
    else:
        form = TrainerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = TrainerLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if username field contains an email
            if '@' in username:
                # Try to authenticate with email
                user = authenticate(request, email=username, password=password)
            else:
                # Try to authenticate with username
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email/username or password.')
    else:
        form = TrainerLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = TrainerProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == "POST":
        # Get the user
        user = request.user

        # Log the user out
        logout(request)

        # Delete the user account
        user.delete()

        # Redirect to home page with a success message
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')

    # If not POST request, show the confirmation page
    return render(request, 'accounts/delete_account.html')