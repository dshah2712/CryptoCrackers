from django import forms
from .models import UserDetails, Wallet, CryptoCurrency, Purchase, Transaction
import json


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', required=True)

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


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
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'autocomplete': 'new-password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)


def _init_(self, *args, **kwargs):
    super(RegisterForm, self)._init_(*args, **kwargs)
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True
    self.fields['email'].required = True
    self.fields['username'].required = True

class JSONSelect(forms.Select):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value


class sellform(forms.ModelForm):
    sellquantity = forms.IntegerField(required=True)

    class Meta:
        model = UserDetails
        fields = ['cryptocurrencies']
        widgets = {
            'cryptocurrencies': forms.Select(attrs={'id': 'id_cryptocurrencies'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the user details for the specified user_id
        user_details = UserDetails.objects.get(id=user_id)

        choices = [(key, key) for key in user_details.cryptocurrencies.keys()]

        self.fields['cryptocurrencies'].widget = forms.Select(choices=choices)

        self.user_id = user_id

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']


class PurchaseForm(forms.ModelForm):
    # quantity = forms.DecimalField(widget=forms.TextInput(attrs={'id': 'id_quantity', 'step': 'any'}))

    class Meta:
        model = Purchase
        fields = ['cryptocurrency', 'quantity']
        widgets = {
            'cryptocurrency': forms.Select(attrs={'id': 'id_cryptocurrency'}),
            'quantity': forms.TextInput(attrs={'id': 'id_quantity'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cryptocurrency'].queryset = CryptoCurrency.objects.all()
        self.user_id = user_id

    def clean(self):
        cleaned_data = super().clean()
        cryptocurrency = cleaned_data.get('cryptocurrency')
        quantity = cleaned_data.get('quantity')
        total_amount = cryptocurrency.current_price_cad * quantity
        cleaned_data['total_amount'] = total_amount
        return cleaned_data


