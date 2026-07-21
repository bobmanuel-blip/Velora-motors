from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import DealerProfile, User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.Role.choices, initial=User.Role.BUYER)
    phone_number = forms.CharField(required=False, max_length=32)

    class Meta:
        model = User
        fields = ["username", "email", "role", "phone_number", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.phone_number = self.cleaned_data.get("phone_number", "")
        if commit:
            user.save()
        return user


class DealerProfileForm(forms.ModelForm):
    class Meta:
        model = DealerProfile
        fields = ["company_name", "description", "logo", "city", "country", "website"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
