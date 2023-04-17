from django import forms

from salon.models import Barbershop
from services.models import Services,ServicePrice
from users.models import Barber


class BookingForm(forms.Form):
    bs = Barbershop.objects.all()
    barbershop = forms.ModelChoiceField(queryset=bs)
    barber = forms.ModelChoiceField(queryset=Barber.objects.all(), empty_label=None)
    service = forms.ModelChoiceField(queryset=ServicePrice.objects.all())
    time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                               widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
