from django.shortcuts import render, redirect

from salon.models import Barbershop
from services.models import ServicePrice, Booking
from users.models import Barber


# def booking(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # перенаправляем пользователя на страницу успеха
#     else:
#         initial = {'barbershop': request.GET.get('barbershop')}  # передаем барбершоп через GET параметр
#         form = BookingForm(initial=initial)
#     return render(request, 'services/booking.html', {'form': form})


def booking(request):
    barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barber = Barber.objects.all().filter(pk=request.GET.get('barber')).first()
    get_service = ServicePrice.objects.all().filter(pk=request.GET.get('service')).first()
    print(get_service)
    context = {'barbershop': barbershop, 'barber': get_barber, "service": get_service}
    return render(request, 'services/booking.html', context)


def barber(request):
    barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barbers = Barber.objects.filter(barbershop_id=request.GET.get('barbershop'))
    get_service = request.GET.get('service')
    print(f'get_service -- {get_service}')
    services = ServicePrice.objects.all().filter(pk=get_service).first()
    print(f'services -- {services}')
    if get_service:
        print(get_barbers.filter(qualification_id=services.qualification_id))
        get_barbers = get_barbers.filter(qualification_id=services.qualification_id)
    print(get_barbers)
    context = {'barbers': get_barbers, 'barbershop': barbershop, "service": services}
    return render(request, 'services/barbers.html', context)


def service(request):
    barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barber = Barber.objects.all().filter(pk=request.GET.get('barber')).first()
    print(f'barber -- {request.GET.get("barber")}')
    if get_barber:
        print('yes')
        barber_qualification = get_barber.qualification_id
        services = ServicePrice.objects.all().filter(qualification=barber_qualification)
    else:
        print('no')
        services = ServicePrice.objects.all()
    print(get_barber)
    context = {'services': services, 'barber': get_barber, 'barbershop': barbershop}
    return render(request, 'services/services.html', context)
