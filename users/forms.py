from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .widgets import CustomClearableFileInput
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username"
        })
    )
    # gender = forms.ChoiceField(
    #     label="Gender",
    #     widget=forms.Select(attrs={"class": "form-control"}),
    #     choices=(("male", "Male"), ("female", "Female"), ("other", "Other")),
    # )
    # phone_number = forms.CharField(
    #     label="Phone Number",
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control",
    #         "placeholder": "Enter your phone number"
    #     }),
    #     max_length=15,
    # )
    # birth_data = forms.DateField(
    #     label="Birth Date",
    #     widget=forms.DateInput(attrs={
    #         "class": "form-control",
    #         "type": "date",
    #         "placeholder": "YYYY-MM-DD"
    #     }),
    #     input_formats=["%Y-%m-%d"],
    # )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm your password"
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


class CustomUserAuthentificationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": "Enter your username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          "placeholder": "Enter your password"})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class CustomUserProfileForm(UserChangeForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True}),

    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", 'readonly': True}),

    )
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    gender = forms.ChoiceField(
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("male", "Male"), ("female", "Female"), ("other", "Other")),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=15,
        required=False,
    )
    birth_data = forms.DateField(
        label="Birth Date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        input_formats=["%Y-%m-%d"],
        required=False,
    )
    profile_img = forms.ImageField(
        label='Your Image',
        widget=forms.FileInput(
            attrs={"class": "form-control-file form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ('profile_img', 'username', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'birth_data')
