from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import CustomUser, phone_regex
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введите свой email"
        })
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите имя пользователя"
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
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль"
        })
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Подтвердите пароль"
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Данная почта уже используется")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже зарегистрирован")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        try:
            validate_password(password2, self.instance)
        except ValidationError as validation_error:
            raise forms.ValidationError(
                "Пароль должен содержать как минимум 8 символов. Попробуйте сочетание строчных и заглавных букв, цифр.")

        if password1 != password2:
            raise forms.ValidationError("Введённые пароли должны совпадать")

        return password2


class CustomUserAuthentificationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": "Введите имя пользователя"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          "placeholder": "Введите пароль"})
    )

    error_messages = {
        'invalid_login': "Введено некорректное имя пользователя или пароль. Обратите внимание, что оба поля могут быть чувствительны к регистру.",
    }

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class CustomUserProfileForm(UserChangeForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True}),

    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", 'readonly': True}),

    )
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    gender = forms.ChoiceField(
        label="Пол",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("Мужской", "Мужской"), ("Женский", "Женский")),
    )
    phone_number = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=15,
        required=False,
        validators=[phone_regex],
    )
    birth_data = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        required=False,
    )
    profile_img = forms.ImageField(
        label='Фото профиля',
        widget=forms.FileInput(
            attrs={"class": "form-control-file form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ('profile_img', 'username', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'birth_data')
