from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # print(form)
        if form.is_valid():
            print("valid")
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            pin_code = form.cleaned_data.get('pin_code')
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            if user:
                user.phone_number = phone_number
                user.country = country
                user.city = city
                user.pin_code = pin_code
                user.save()

                current_site = get_current_site(request)
                mail_subject = "Please Activate Your Account"
                message = render_to_string(
                    'accounts/account_verification_email.html', {
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                messages.success(request, "Registration successful")
            return redirect('activate')
        else:
            print(form.errors)
            for errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/registration.html', context)


def activate(request):
    # success_message = messages.get_messages(request)
    # messages_list = [m for m in success_message]
    # context = {
    #     'success_message': messages_list[0].message if messages_list else None
    # }
    return render(request, 'accounts/activate.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not Account.objects.filter(email=email).exists():
            messages.error(
                request, "Account not found")
            return redirect('login')

        else:
            user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request, "Please verify your account before logging in!!!")
                return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def signout(request):
    logout(request)
    return render(request, 'accounts/login.html')
