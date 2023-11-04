from django.shortcuts import render,redirect,get_object_or_404
from .forms import  LoginForm,RegisterForm,ForgotPasswordForm, PurchaseForm
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import UserDetails,CryptoCurrency, Transactions
from django.http import HttpResponse
def index(request):
    # fetch_and_store_crypto_data()
    if request.user.is_authenticated:
        # Access user data from Google OAuth
        google_account = request.user.socialaccount_set.filter(provider='google').first()

        if google_account:

            google_data = google_account.extra_data
            print("google account details", google_data)
            google_email = google_data.get('email')
            try:
                user = UserDetails.objects.get(username=google_email)
                if user:
                    print("User exist")
                else:
                    print("User does not else exist")

            except UserDetails.DoesNotExist:
                newGoogleUser = UserDetails(username=google_email,first_name=google_data.get('given_name'),last_name=google_data.get('family_name'),email=google_email)
                newGoogleUser.save()
                print("New User created")

    coin_list = CryptoCurrency.objects.all().order_by('market_cap_rank')[:10]
    print(coin_list)

    return render(request, 'FrontEnd/index.html',{'coins': coin_list})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = UserDetails.objects.get(username=username)
                print("user details are:",user.password)
                if user:
                    if user.password is None:
                        form.add_error(None, 'Google Auth Sign In Required')
                    else:
                        if check_password(password, user.password):
                            # Manually set the user's ID in the session to log them in
                            request.session['_user_id'] = user.id
                            return redirect('/')
                        else:
                            form.add_error(None, 'Invalid login credentials')

            except UserDetails.DoesNotExist:
                form.add_error(None, 'User does not exist')
    else:
        form = LoginForm()
    return render(request, 'FrontEnd/login.html', {'form': form})


def process_form(request):
    print("inside process form")
    if request.method == 'POST':
        # Get form data from request.POST
        print("all data",request.POST)
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


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request.FILES)

        # print("forgot password")
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            try:
                user = UserDetails.objects.get(username=username)
                print("user details are:",user.password)

                if user.password is None:
                        form.add_error(None, 'Google Auth Sign In Required')
                else:
                    if password == confirm_password:
                        print("pass match")
                        user.password = make_password(password)
                        user.save()
                        # print("new pass: ",user.password)
                        return redirect('/login/')
                    else:
                        print("pass not match")
                        form.add_error(None, 'Password does not match')
            except UserDetails.DoesNotExist:
                form.add_error(None, 'User does not exist')


    else:
        form = ForgotPasswordForm()
    return render(request, 'FrontEnd/forgotpassword.html', {'form': form})


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
