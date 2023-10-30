from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import  LoginForm,RegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import UserDetails,CryptoCurrency

from django.http import HttpResponse
def index(request):
    if request.user.is_authenticated:
        # Access user data from Google OAuth
        google_account = request.user.socialaccount_set.filter(provider='google').first()

        if google_account:

            google_data = google_account.extra_data
            print("google account details", google_data)
            google_email = google_data.get('email')
            google_name = google_data.get('name')
    coin_list = CryptoCurrency.objects.all().order_by('market_cap_rank')[:10]
    print(coin_list)

    return render(request, 'FrontEnd/index.html',{'coins': coin_list})

# def login(request):
#     return render(request, 'FrontEnd/login.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = UserDetails.objects.get(username=username)
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