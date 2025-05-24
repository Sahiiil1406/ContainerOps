from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password'] 
        labels = {
            'email': 'Email',
            'username': 'Create Username',
            'password': 'Create Password',
        }
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not password or not confirm_password:
            raise forms.ValidationError("Both password and confirm password fields are required.")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    


