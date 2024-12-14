from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q


class UserFormRegistration(UserCreationForm):
    class Meta:
        fields = ["username", "email", "password1", "password2"]
        model = get_user_model()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        try:
            if get_user_model().objects.get(email=username):
                raise ValidationError("Username already exists")
        except get_user_model().DoesNotExist:
            return cleaned_data

        return cleaned_data


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or E-Mail", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")

        try:
            user = get_user_model().objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except get_user_model().DoesNotExist:
            raise ValidationError("Username or password is incorrect")

        if not user.check_password(password):
            raise ValidationError("Username or password is incorrect")

        cleaned_data["user"] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get("user")


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "description", "photo"]


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = get_user_model()
        fields = ["password"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if not password:
            raise ValidationError("Password is required")

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match")

        if not self.user.check_password(password):
            raise ValidationError("Incorrect password")

        return cleaned_data


class ChangeEmailForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    new_email = forms.CharField(widget=forms.TextInput, label="New E-Mail")

    class Meta:
        model = get_user_model()
        fields = ["password", "new_email"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("new_email")
        if not self.user.check_password(cleaned_data.get("password")):
            return ValidationError("Invalid password.")

        if not password:
            raise ValidationError("Password is required")

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("E-Mail already exists")

        return cleaned_data


class ResetPasswordConfirmForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
