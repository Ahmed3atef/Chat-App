from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.contrib.auth import logout

from allauth.account.models import EmailAddress
from . import forms

User = get_user_model()

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    form = forms.ProfileForm(instance=request.user.profile)
    
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'users/profile_edit.html', {'form': form, 'onboarding': onboarding})


@login_required
def profile_settings_view(request):
    return render(request, 'users/profile_settings.html')


@login_required
def profile_emailchange(request):

    if request.htmx:
        form = forms.EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = forms.EmailForm(request.POST, instance=request.user)

        if form.is_valid():

            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')

            form.save()

            try:
                email_address = EmailAddress.objects.get(user=request.user, email__iexact=form.cleaned_data['email'])
                email_address.send_confirmation(request)
            except EmailAddress.DoesNotExist:
                # If the signal didn't create the EmailAddress, create it now
                EmailAddress.objects.add_email(request, request.user, form.cleaned_data['email'], confirm=True)

            return redirect('profile-settings')
        else:
            messages.warning(request, 'Email not valid or already in use')
            return redirect('profile-settings')

    return redirect('profile-settings')


@login_required
def profile_emailverify(request):
    try:
        email_address = EmailAddress.objects.get(user=request.user, email__iexact=request.user.email)
        if not email_address.verified:
            email_address.send_confirmation(request)
            messages.success(request, f"A verification email has been sent to {email_address.email}.")
        else:
            messages.info(request, "Your email address is already verified.")
    except EmailAddress.DoesNotExist:
        EmailAddress.objects.add_email(request, request.user, request.user.email, confirm=True)
        messages.success(request, f"A verification email has been sent to {request.user.email}.")

    return redirect("profile-settings")


@login_required
def profile_usernamechange(request):
    if request.htmx:
        form = forms.UsernameForm(instance=request.user)
        return render(request, 'partials/username_form.html', {'form': form})

    if request.method == 'POST':
        form = forms.UsernameForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Username updated successfully.')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Username not valid or already in use')
            return redirect('profile-settings')

    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

    return render(request, 'users/profile_delete.html')
