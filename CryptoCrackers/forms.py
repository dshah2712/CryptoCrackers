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


class sellform(forms.Form):

    cryptocurrencies = forms.ChoiceField(choices=[])
    sell_quantity = forms.IntegerField(required=True)

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check which user we need the keys
        user_details = UserDetails.objects.get(id=user_id)

        # Take data for that user
        crypto_dict = user_details.cryptocurrencies

        choices = [(key, key) for key in crypto_dict.keys()]

        self.fields['cryptocurrencies'].choices = choices

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



# class PortfolioTransactionForm(forms.ModelForm):
#     action = forms.ChoiceField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
#     coin = forms.ModelChoiceField(queryset=CryptoCurrency.objects.all())
#     quantity = forms.IntegerField()

#     class Meta:
#         model = portfolioTranscation
#         fields = ['action', 'coin', 'quantity']

#     def clean_quantity(self):
#         action = self.cleaned_data['action']
#         quantity = self.cleaned_data['quantity']

#         if action == 'SELL' and quantity > 0:
#             raise forms.ValidationError('Quantity should be negative for sell transactions.')

#         return quantity

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields  = ['username', 'first_name', 'last_name', 'date_of_birth']