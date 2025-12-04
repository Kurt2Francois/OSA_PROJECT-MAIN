from django import forms
from .models import User, Department

class UserRegistrationForm(forms.ModelForm):
    """Form for user registration"""
    confirm_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    
    class Meta:
        model = User
        fields = ['business_email', 'department_name', 'contact_person', 'contact_number', 'email']
        widgets = {
            'business_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Business Email'}),
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Email addresses do not match")
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class LoginForm(forms.Form):
    """Form for user login"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class DepartmentForm(forms.ModelForm):
    """Form for department editing"""
    class Meta:
        model = Department
        fields = ['department_name', 'business_email', 'email', 'logo_path', 
                  'established_date', 'expiration_date', 'partnership_status', 'remarks_status']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'partnership_status': forms.Select(attrs={'class': 'form-control'}),
            'remarks_status': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo_path': forms.FileInput(attrs={'class': 'form-control'}),
        }