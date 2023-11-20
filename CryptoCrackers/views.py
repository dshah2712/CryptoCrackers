import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, PurchaseForm, AddMoneyForm,ChangePasswordForm
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import UserDetails, CryptoCurrency, News, Wallet, Purchase, Transaction
import matplotlib as mpl
import random
mpl.use('Agg')  # Use the 'Agg' backend, which is non-interactive and works well in various environments
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
def index(request):
    news = News.objects.all()
    a  = False
    value = request.session.get('_user_id')
    wish_list = []
    user = None
    user_log = False
    my_var = request.session.get('_user_id')
    if my_var:
        user_log = True
        user = UserDetails.objects.get(id=value)
        wish_list = user.wishlist


    else:
        user_log = False
    if request.user.is_authenticated:
        # Access user data from Google OAuth

        google_account = request.user.socialaccount_set.filter(provider='google').first()

        if google_account:

            google_data = google_account.extra_data
            print("google account details", google_data)
            google_email = google_data.get('email')

            # print("email",google_email)
            try:
                user = UserDetails.objects.get(username=google_email)
                request.session['_user_id'] = user.id
                print("google id user details", user)
                wish_list = user.wishlist
                if user:
                    print("User exist")
                else:
                    print("User does not else exist")

            except UserDetails.DoesNotExist:
                newGoogleUser = UserDetails(username=google_email, first_name=google_data.get('given_name'),
                                            last_name=google_data.get('family_name'), email=google_email)
                newGoogleUser.save()
                print("New User created")

    coin_list = CryptoCurrency.objects.all().order_by('market_cap_rank')[:20]
    print("user details are: ", user)

    # print(coin_list)
    if request.user.is_authenticated:
        user_log = True

    return render(request, 'FrontEnd/index.html',
                  {'user': user, 'coins': coin_list, 'user_log': user_log, 'news': news, 'wish_list': wish_list})


def landing(request):
    return render(request, 'FrontEnd/landingPage.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = UserDetails.objects.get(username=username)
                print("user details are:", user.password)
                if user:
                    if user.password is None:
                        form.add_error(None, 'Google Auth Sign In Required')
                    else:
                        if check_password(password, user.password):
                            # Manually set the user's ID in the session to log them in
                            request.session['_user_id'] = user.id

                            return redirect('CryptoCrackers:index')
                            # # Redirect to the user's profile page
                            # return HttpResponseRedirect(reverse('CryptoCrackers:profile'))
                        else:
                            form.add_error(None, 'Invalid login credentials')
                            return redirect('/login')
                # else:
                #     form.add_error(None, 'User Does Not Exist')
                #     return redirect('/')                    

            except UserDetails.DoesNotExist:
                form.add_error(None, 'User does not exist')
                return redirect('/login')     
    else:
        form = LoginForm()
        return render(request, 'FrontEnd/login.html', {'form': form})


def process_form(request):
    print("inside process form")
    if request.method == 'POST':
        # Get form data from request.POST
        print("all data", request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        # Redirect to a success page or another appropriate URL
        return redirect('CryptoCrackers:index')
    else:
        # Handle GET requests or other HTTP methods if needed
        return render(request, 'FrontEnd/login.html')


def user_signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(request, 'FrontEnd/signup.html', {'form': form})



def send_forgotpassword_mail(request):
    print("forgot pass clicked")

    return HttpResponseRedirect(reverse('CryptoCrackers:forgotpassword'))

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print("email entered is: ",email)
            try:

                email_user = UserDetails.objects.get(email=email)
                if email_user.password is None:
                    form.add_error(None, 'Google Auth Sign In Required')
                else:
                    otp = random.randint(100000, 999999)
                    request.session['otp'] = otp
                    message = "This is the " + str(otp) + "."
                    send_mail(
                        "One-Time Password",
                        message,
                        settings.EMAIL_HOST,
                        [email],
                        fail_silently=False,
                    )
                    return HttpResponseRedirect(reverse('CryptoCrackers:changepassword'))
            except UserDetails.DoesNotExist:
                form.add_error(None, 'Enter correct email id')

    else:
        form = ForgotPasswordForm()
    return render(request, 'FrontEnd/forgotpassword.html', {"form": form})




def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request.FILES)
        print("details: ",request.POST.get('email'))

        print("forgot password")
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            otp = form.cleaned_data['otp']
            try:
                user = UserDetails.objects.get(username=username)
                print("user details are:", user.password)

                if user.password is None:
                    form.add_error(None, 'Google Auth Sign In Required')
                else:
                    if request.session.get('otp') and otp == request.session.get('otp'):

                        if password == confirm_password:
                            print("pass match")
                            user.password = make_password(password)
                            user.save()
                            # print("new pass: ",user.password)
                            return redirect('/login/')
                        else:
                            print("pass not match")
                            form.add_error(None, 'Password does not match')
                    else:
                        form.add_error(None, 'OTP does not match')
            except UserDetails.DoesNotExist:
                form.add_error(None, 'User does not exist')


    else:
        form = ChangePasswordForm()
    return render(request, 'FrontEnd/changepassword.html',{"form":form})



def create_transaction(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Don't save the form yet because we haven't completed the payment
            transaction = form.save(commit=False)

            # Get the current price of the selected cryptocurrency in CAD
            current_price_cad = transaction.currency.current_price_cad

            # Calculate the total price
            total_price = transaction.amount * current_price_cad

            # You may want to store the transaction in the session or a temporary place
            request.session['transaction_data'] = {
                'currency_id': transaction.currency.id,
                'amount': str(transaction.amount),
                'total_price': str(total_price)
            }

            # Redirect to the payment page
            return redirect('/payment/')
    else:
        form = PurchaseForm()
    return render(request, 'FrontEnd/purchase_form.html', {'form': form})


def purchase_crypto(request):
    # Retrieve the transaction data from the session
    transaction_data = request.session.get('transaction_data', {})

    # In a real application, you should clear the session data after use
    # request.session.pop('transaction_data', None)

    context = {
        'total_price': transaction_data.get('total_price'),
        'currency_id': transaction_data.get('currency_id'),
        'amount': transaction_data.get('amount'),
    }
    return render(request, 'FrontEnd/payment.html', context)




def dynamic_Crypto(request, coin_name):

    coin = get_object_or_404(CryptoCurrency, name=coin_name)
    plt.switch_backend('Agg')
    if coin.current_price < 1:
        coin.current_price = 10 + coin.current_price
    base_value = int(coin.current_price)

    # Generate 12 monthly values that depend on the base value, for example, fluctuate by up to 15%
    monthly_changes = np.random.uniform(-0.15, 0.15, 12)
    monthly_values = base_value * (1 + monthly_changes)

    # Generate a date range of the last 12 months
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, periods=12, freq='MS')  # 'MS' stands for month start frequency

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, monthly_values, color='darkorange', marker='o', linewidth=2)

    # Format the dates on the x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.xticks(rotation=45)

    # Set y-axis range to ±15% from the base value
    y_min = base_value * (1 - 0.2)
    y_max = base_value * (1 + 0.2)
    ax.set_ylim([y_min, y_max])

    # Hide the y-axis labels and spines
    # ax.get_yaxis().set_visible(False)
    # for spine in ax.spines.values():
    #     spine.set_visible(False)

    # Hide the y-axis
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    # ax.spines['bottom'].set_linewidth(0)
    # current_price = prices[-1]
    # price_change =
    percentage_change = .15 * 100
    # Use ax.text() to add annotations to the plot
    ax.text(0.03, 0.97, f'USD${coin.current_price:,.2f}',
            transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.3))

    ax.text(0.03, 0.92, f'↗USD${15:,.2f} ({percentage_change:.2f}%)',
            transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.3))

    # Remaining plot code...

    # Convert plot to PNG image
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    buf.seek(0)  # Rewind the buffer

    # Encode the image in base64 and close the buffer
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Construct the image src data URI
    image_url = f"data:image/png;base64,{image_base64}"
    context = {
        "coin": coin,
        "data_uri": image_url
    }

    return render(request, 'FrontEnd/dynamicCrypto.html', context)



def user_profile(request):
    if request.method == 'POST':
        print(request.POST['avatar'])
        value = request.session.get('_user_id')
        # Get user details from the retrieved user id
        user = UserDetails.objects.get(id=value)
        user.first_name = request.POST['firstname']
        user.username = request.POST['username']
        user.last_name = request.POST['lastname']
        user.save()
        return render(request, 'FrontEnd/profile.html', {'user': user})
    else:
        # Retrieve the user id from the session
        value = request.session.get('_user_id')
        # Get user details from the retrieved user id
        user = UserDetails.objects.get(id=value)

        wish_list = user.wishlist
        return render(request, 'FrontEnd/profile.html', {'user': user, 'wish_list': wish_list})
        # return render(request, 'FrontEnd/profile.html', {'user': user})




def passwd_change(request):
    value = request.session.get('_user_id')
    user = UserDetails.objects.get(id=value)

    currentPassword = request.POST['current-password']
    if check_password(currentPassword, user.password):
        if (request.POST['new-password'] == request.POST['confirm-password']):
            user.password = make_password(request.POST['new-password'])
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('/userprofile')
        else:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('/userprofile')
    else:
        messages.error(request, "Current password is incorrect")
        return redirect('/userprofile')


def delete_account(request):
    if request.method == 'POST':
        value = request.session.get('_user_id')
        user = UserDetails.objects.get(id=value)
        user.delete()
        request.session.flush()
        return redirect('/')

    return HttpResponse("Invalid request method", status=405)



def user_logout(request):
    request.session.flush()
    logout(request)
    # messages.success(request,("You Were Logged Out Successfully!"))
    return redirect('/')



def wishlist(request):
    value = request.session.get('_user_id')
    if not value:
        # Redirect to login or handle the case where the user is not authenticated
        return redirect('/login/')
    user = UserDetails.objects.get(id=value)
    wish_list = user.wishlist
    print(wish_list)

    return render(request, 'FrontEnd/profile.html',{"user":user, 'wish_list':wish_list })
    # return render(request, 'FrontEnd/wishlist.html', {"user": user, 'wish_list': wish_list})



def add_to_wishlist(request, coin_name):
    value = request.session.get('_user_id')
    if not value:
        # Redirect to login or handle the case where the user is not authenticated
        return redirect('/login/')
    user = UserDetails.objects.get(id=value)
    coin = get_object_or_404(CryptoCurrency, name=coin_name)
    user.wishlist.append(coin.name)
    user.save()

    print("wishlist added", user)
    return redirect('CryptoCrackers:index')


def remove_to_wishlist(request, coin_name):
    value = request.session.get('_user_id')
    user = UserDetails.objects.get(id=value)


    if coin_name in user.wishlist:
        user.wishlist.remove(coin_name)
        user.save()
        print("wishlist removed", user)
    else:
        print(f"{coin_name} not found in wishlist")

    # Redirect to the profile or another appropriate URL
    return redirect('/')
    print("wishlist removed", user)
    return redirect('CryptoCrackers:index')


def add_money(request):
    user_id = request.session.get('_user_id')
    if not user_id:
        # Redirect to login or handle the case where the user is not authenticated
        return redirect('/login/')

    user_wallet, created = Wallet.objects.get_or_create(user_id=user_id)

    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # currency = form.cleaned_data['currency']

            user_wallet.balance += amount
            user_wallet.save()

            Transaction.objects.create(
                user_id=user_id,
                # currency=currency,
                amount=amount,
                transaction_type='deposit',
            )

            return JsonResponse({'success': True})

    else:
        form = AddMoneyForm()

    balance = user_wallet.balance
    return render(request, 'FrontEnd/add_money.html', {'form': form, 'balance': balance})


def purchase_currency(request):
    user_id = request.session.get('_user_id')
    if not user_id:
        # Redirect to login or handle the case where the user is not authenticated
        return redirect('/login/')

    user_wallet, created = Wallet.objects.get_or_create(user_id=user_id)

    if request.method == 'POST':
        form = PurchaseForm(user_id, request.POST)

        if form.is_valid():
            cryptocurrency = form.cleaned_data['cryptocurrency']
            quantity = form.cleaned_data['quantity']
            total_amount = cryptocurrency.current_price_cad * quantity
            print("total amt; ",total_amount)
            print("userBalance: ",user_wallet.balance)
            if user_wallet.balance >= total_amount:
                user_wallet.balance -= total_amount
                user_wallet.save()

                Purchase.objects.create(
                    user_id=user_id,
                    cryptocurrency=cryptocurrency,
                    quantity=quantity,
                    total_amount=total_amount,
                )
                print("successfull")
                return JsonResponse({'success': True})

            else:
                print("failed")
                return JsonResponse({'success': False})
    else:
        form = PurchaseForm(user_id)

        # Fetch the cryptocurrency choices and pass them to the template as a JSON string
        crypto_choices = [{'id': crypto.id, 'name': crypto.name, 'price': str(crypto.current_price_cad)} for crypto in
                          CryptoCurrency.objects.all()]
        crypto_choices_json = json.dumps(crypto_choices, cls=DjangoJSONEncoder)

        return render(request, 'FrontEnd/purchase_currency.html',
                      {'form': form, 'balance': user_wallet.balance, 'crypto_choices_json': crypto_choices_json})

