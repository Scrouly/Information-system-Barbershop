from django import forms

from salon.models import Barbershop
from services.models import Services, ServicePrice, Booking
from users.models import Barber


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': True}),
            'barbershop': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'barber': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'readonly': True}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'readonly': True}),

        }

# class BookingForm(forms.Form):
#     barbershop = forms.CharField(
#         label="Username",
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Enter your username"
#         })
#     )
#     class Meta:
#         model = Booking
#         fields = ('barbershop',)
# bs = Barbershop.objects.all()
# barbershop = forms.ModelChoiceField(queryset=bs)
# barber = forms.ModelChoiceField(queryset=Barber.objects.all(), empty_label=None)
# service = forms.ModelChoiceField(queryset=ServicePrice.objects.all())
# time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
#                            widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
