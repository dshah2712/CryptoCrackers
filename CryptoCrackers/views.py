from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
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

    return render(request, 'FrontEnd/index.html')

def login(request):
    return render(request, 'FrontEnd/login.html')


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


def signup(request):
    return render(request, 'FrontEnd/signup.html')