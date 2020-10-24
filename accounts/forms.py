from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))

# Sign up page for Job seeker 
class EmployeeRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        # 7 fields to fill in employee registration page

        self.fields['password1'] = forms.CharField(label='Password',widget=forms.PasswordInput)

        self.fields['user_gender'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['first_name'].widget.attrs['class']='form-control'
        self.fields['first_name'].widget.attrs['id'] = 'id_first_name'
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['user_link'].label = "LinkedIn URL"
        self.fields['user_link'].widget = forms.URLInput()

        # Place holder description for all fields
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter your First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter your Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter your Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter the Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm the Password',
            }
        )
        self.fields['user_link'].widget.attrs.update(
            {
                'placeholder': 'Enter URL for Linkedin',
            }
        )

    # Validations for required fields in registration form
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'user_link', 'user_gender']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'user_gender': {
                'required': 'Gender is required'
            }
        }
        help_texts = {
            'password1':None,
        }
        # widgets = {
        #     'first_name':forms.TextInput(attrs={'class':'form-control'})
        # }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_employee = True
        user.is_employer = False
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['company_name'].label = "Company Name"
        self.fields['company_address'].label = "Company Address"


        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Address',
            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['company_address'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'company_name', 'company_address', 'email', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_employer = True
        user.is_employee = False
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Invalid Username / Password")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

