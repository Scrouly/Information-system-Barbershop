import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from salon.models import Barbershop
from django.urls import reverse
from services.forms import BookingForm
from services.models import ServicePrice, Booking, WorkingTime
from users.models import Barber, CustomUser


def booking_success(request):
    user_booking = Booking.objects.filter(customer__username=request.user).order_by('-creation_time').first()
    context = {'booking': user_booking, }
    # context = {'barbershop': barbershop, 'barber': get_barber, "service": get_service, 'appointment': get_appointment}
    return render(request, 'services/booking_confirmation.html', context)


def booking(request):
    print(f"--GET--{request.GET}")
    print(f"--POST--{request.POST}")
    get_user = get_object_or_404(CustomUser, username=request.user)
    print(get_user)
    barbershop = Barbershop.objects.filter(pk=request.GET.get('barbershop')).first()
    get_barber = Barber.objects.all().filter(pk=request.GET.get('barber')).first()
    get_service = ServicePrice.objects.all().filter(pk=request.GET.get('service')).first()
    get_appointment = request.GET.get('appointment')
    form = BookingForm()
    # if request.method == "GET":
    # if get_appointment:
    #     date_str, time_str = '-'.join(get_appointment.split('-')[:3]), get_appointment.split('-')[3]
    # print(time_str)
    # init = {'customer': get_user,
    #         'barbershop': barbershop,
    #         'barber': get_barber,
    #         'service': get_service,
    #         'appointment_date': date_str,
    #         'appointment_time': get_object_or_404(WorkingTime, hour__exact=time_str+":00"), }
    # print(get_object_or_404(WorkingTime, hour__exact=time_str))
    # print(Barbershop.objects.filter(pk=request.GET.get('barbershop')).first())
    # form = BookingForm(init)
    # print(form.data)
    # print('gg')

    if request.method == "POST":
        date_str, time_str = '-'.join(get_appointment.split('-')[:3]), get_appointment.split('-')[3]
        init = {'customer': get_user,
                'barbershop': barbershop,
                'barber': get_barber,
                'service': get_service,
                'appointment_date': date_str,
                'appointment_time': get_object_or_404(WorkingTime, hour__exact=time_str + ":00"), }
        form = BookingForm(init)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('services:success'))
            print('gg WP')
    context = {'barbershop': barbershop, 'barber': get_barber, "service": get_service, 'appointment': get_appointment,
               'form': form}
    return render(request, 'services/booking.html', context)


def barber(request):
    barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barbers = Barber.objects.filter(barbershop_id=request.GET.get('barbershop'))
    get_service = request.GET.get('service')
    get_appointment = request.GET.get('appointment')
    services = ServicePrice.objects.all().filter(pk=get_service).first()
    if get_appointment:
        date_str, time_str = '-'.join(get_appointment.split('-')[:3]), get_appointment.split('-')[3]
        print(date_str, time_str)
        get_barbers = get_barbers.exclude(booking__appointment_date=date_str, booking__appointment_time__hour=time_str)
    if get_service:
        get_barbers = get_barbers.filter(qualification_id=services.qualification_id)
    context = {'barbers': get_barbers, 'barbershop': barbershop, "service": services, 'appointment': get_appointment}
    return render(request, 'services/barbers.html', context)


def service(request):
    barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barber = Barber.objects.all().filter(pk=request.GET.get('barber')).first()
    get_appointment = request.GET.get('appointment')
    if get_barber:
        barber_qualification = get_barber.qualification_id
        services = ServicePrice.objects.all().filter(qualification=barber_qualification)
    else:
        services = ServicePrice.objects.all()
    context = {'services': services, 'barber': get_barber, 'barbershop': barbershop, 'appointment': get_appointment}
    return render(request, 'services/services.html', context)


def appointment(request):
    get_barbershop = Barbershop.objects.get(pk=request.GET.get('barbershop'))
    get_barber = Barber.objects.all().filter(pk=request.GET.get('barber')).first()
    get_service = ServicePrice.objects.all().filter(pk=request.GET.get('service')).first()
    today = datetime.date.today()
    day_list = []
    working_time = WorkingTime.objects.all()
    for i in range(7):
        day = {}
        curr_day = today + datetime.timedelta(days=i)
        weekday = curr_day.strftime("%A").upper()
        day["date"] = str(curr_day)
        day["day"] = weekday
        b = Booking.objects.filter(barber=get_barber, appointment_date=f'{curr_day}')
        if b:
            day['free_time'] = WorkingTime.objects.exclude(pk__in=[x.appointment_time_id for x in b])
        else:
            day['free_time'] = working_time
            print(working_time)
        if today == curr_day:
            curr_time = int(datetime.datetime.now().strftime("%H"))
            for time in day['free_time']:
                print(f"time--{time.hour.strftime('%H')}")
                if int(time.hour.strftime('%H')) <= curr_time:
                    day['free_time'] = day['free_time'].exclude(hour=time.hour)
        if day['free_time']:
            day_list.append(day)
    context = {'appointment': day_list, 'service': get_service, 'barber': get_barber, 'barbershop': get_barbershop}
    return render(request, 'services/appointment.html', context)


def delete_booking(request, pk):
    get_booking = get_object_or_404(Booking, pk=pk, customer=request.user, completed=False)
    if request.method == 'POST':
        get_booking.delete()
        messages.success(request, 'Запись была отменена')
        return redirect('users:profile')
    return render(request, 'services/delete_booking.html', {'booking': get_booking})
