from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['profile_image','full_name', 'email', 'password1', 'password2']

        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profile_image'].help_text = None
        self.fields['profile_image'].label = "Profile Image"