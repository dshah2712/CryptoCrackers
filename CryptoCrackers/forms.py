import re

from django import forms
from .models import UserDetails, CryptoCurrency, Purchase, Transaction



class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        min_length=5,
        max_length=10,
        help_text='Your password must be between 5 - 10 characters. It must contain at least one special character, one uppercase letter, one lowercase letter and one numeric digit.'
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password',
        required=True,
        min_length=5,
        max_length=10
    )

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

        return password_confirm

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Ensure the password contains at least one special character
        if not re.match(r'^(?=.*[!@#$%^&*()_+\-=\[\]{};:\'",<>./?\\|`~])(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{5,10}$',
                        password):
            raise forms.ValidationError('Password must meet the specified criteria.')

        return password

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class AccountSecurity(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)


class ChangePasswordForm(forms.Form):
    username = forms.CharField(required=True)
    otp = forms.IntegerField(
        label='Enter a 6-digit number',
        min_value=100000,
        max_value=999999,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a 6-digit number'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'autocomplete': 'new-password'}),
        max_length=20

    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password again','autocomplete': 'new-password'}),
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)


class sellform(forms.Form):

    cryptocurrencies = forms.ChoiceField(choices=[])
    sell_quantity = forms.IntegerField(required=True)

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check which user we need the keys
        user_details = UserDetails.objects.get(id=user_id)

        # Take data for that user
        crypto_dict = user_details.cryptocurrencies

        choices = [(key, f"{key} ({value})") for key, value in crypto_dict.items()]

        self.fields['cryptocurrencies'].choices = choices

        self.user_id = user_id

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    widgets = {
        'amount': forms.NumberInput(),
    }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be a positive number.')

            # Check if amount has more than 10 digits
        if len(str(amount)) > 10:
            raise forms.ValidationError('Amount cannot be greater than 10 digits.')

        return amount


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = ['cryptocurrency', 'quantity']
        widgets = {
            'cryptocurrency': forms.Select(),
            'quantity': forms.NumberInput(),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be a positive number.')
        return quantity

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cryptocurrency'].queryset = CryptoCurrency.objects.all()
        self.user_id = user_id

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'first_name', 'last_name']