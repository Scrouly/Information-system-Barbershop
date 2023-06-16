import datetime
from django.shortcuts import render, get_object_or_404

from reviews.models import Review
from salon.models import Barbershop
from services.models import Booking, WorkingTime
from users.models import Barber
from .utils import revenue_and_customers, difference, graph, dict_for_pie, back_dates, daily_graph
from django.contrib.auth.decorators import permission_required


@permission_required('users.add_barber')
def stats_info(request, pk, barber_pk=None):
    today = datetime.date.today()
    barbershop = get_object_or_404(Barbershop, pk=pk)
    all_barbers = Barber.objects.filter(barbershop=barbershop)
    barber = Barber.objects.filter(pk=barber_pk, barbershop_id=pk).first()
    full_path = request.get_full_path()
    interim = {'interim': "today"}

    if 'week' in full_path or 'month' in full_path:

        if 'week' in full_path:
            last_week = today - datetime.timedelta(days=6)
            previous_week = last_week - datetime.timedelta(days=6)
            interim['interim'] = "week"

        else:
            last_week = today - datetime.timedelta(days=29)
            previous_week = last_week - datetime.timedelta(days=29)
            interim['interim'] = "month"

        this_week_all_dates = back_dates(today, last_week)
        previous_week_all_dates = back_dates(last_week, previous_week)

        if barber_pk:
            week_appointments = Booking.objects.filter(appointment_date__in=this_week_all_dates, barbershop_id=pk,
                                                       barber_id=barber_pk)
            previous_week_appointments = Booking.objects.filter(appointment_date__in=previous_week_all_dates,
                                                                barbershop_id=pk, barber_id=barber_pk)
        else:
            week_appointments = Booking.objects.filter(appointment_date__in=this_week_all_dates, barbershop_id=pk,
                                                       )
            previous_week_appointments = Booking.objects.filter(appointment_date__in=previous_week_all_dates,
                                                                barbershop_id=pk)

        current_appointments = [daily_appointments for daily_appointments in week_appointments]
        previous_appointments = [daily_appointments for daily_appointments in previous_week_appointments]
    else:
        if barber_pk:
            current_appointments = Booking.objects.filter(appointment_date=today, barbershop_id=pk, barber_id=barber_pk)
            previous_appointments = Booking.objects.filter(appointment_date=(today - datetime.timedelta(days=1)),
                                                           barbershop_id=pk, barber_id=barber_pk)
        else:
            current_appointments = Booking.objects.filter(appointment_date=today, barbershop_id=pk)
            previous_appointments = Booking.objects.filter(appointment_date=(today - datetime.timedelta(days=1)),
                                                           barbershop_id=pk)

    get_barbers = [app.barber.user.username for app in current_appointments]
    barber_productivity = dict_for_pie(get_barbers)

    if 'week' in full_path or 'month' in full_path:
        start_date = datetime.datetime.strptime(this_week_all_dates[-1], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(this_week_all_dates[0], '%Y-%m-%d').date() + datetime.timedelta(days=1)
        if not barber_pk:
            current_reviews = [
                rating.rating for rating in Review.objects.filter(
                    barber__barbershop_id=pk,
                    created_time__gte=start_date,
                    created_time__lte=end_date,
                )
            ]
        else:
            current_reviews = [
                rating.rating for rating in Review.objects.filter(
                    barber__barbershop_id=pk,
                    barber_id=barber_pk,
                    created_time__gte=start_date,
                    created_time__lte=end_date,
                )
            ]
    else:
        start_of_day = datetime.datetime.combine(today, datetime.datetime.min.time())
        end_of_day = datetime.datetime.combine(today, datetime.datetime.max.time())
        if not barber_pk:
            current_reviews = [
                rating.rating for rating in Review.objects.filter(
                    barber__barbershop_id=pk,
                    created_time__range=(start_of_day, end_of_day)
                )
            ]
        else:
            current_reviews = [
                rating.rating for rating in Review.objects.filter(
                    barber__barbershop_id=pk,
                    barber_id=barber_pk,
                    created_time__range=(start_of_day, end_of_day),
                )
            ]

    reviews_info = dict(sorted(dict_for_pie(current_reviews).items(), key=lambda x: float(x[0])))

    time = WorkingTime.objects.all()

    try:
        current_average_rating = round(sum(current_reviews) / len(current_reviews), 2)
    except ZeroDivisionError:
        current_average_rating = 0

    current_revenue, current_customers = revenue_and_customers(current_appointments)
    previous_revenue, previous_customers = revenue_and_customers(previous_appointments)

    appointments_difference = difference(len(current_appointments), len(previous_appointments))
    customers_difference = difference(current_customers, previous_customers)
    revenue_difference = difference(current_revenue, previous_revenue)

    max_load_hours = [times.hour.strftime("%H:%M") for times in time]
    max_load_per_interim = graph(
        current_appointments,
        max_load_hours)[0]

    if 'week' in full_path or 'month' in full_path:
        time = this_week_all_dates
        current_appointments_per_interim, current_revenue_per_interim, current_customers_per_interim = daily_graph(
            current_appointments,
            time)
        previous_appointments_per_interim, previous_revenue_per_interim, previous_customers_per_interim = daily_graph(
            previous_appointments, previous_week_all_dates)
    else:
        time = [times.hour.strftime("%H:%M") for times in time]
        current_appointments_per_interim, current_revenue_per_interim, current_customers_per_interim = graph(
            current_appointments,
            time)
        previous_appointments_per_interim, previous_revenue_per_interim, previous_customers_per_interim = graph(
            previous_appointments, time)

    context = {'barber': barber, 'barbershop': barbershop, 'current_appointments': len(current_appointments),
               'current_revenue': current_revenue,
               'current_customers': current_customers, 'appointments_difference': appointments_difference,
               'customers_difference': customers_difference,
               'revenue_difference': revenue_difference, 'time': time,

               'current_appointments_per_interim': current_appointments_per_interim,
               'current_revenue_per_interim': current_revenue_per_interim,
               'current_customers_per_interim': current_customers_per_interim,

               'previous_appointments_per_interim': previous_appointments_per_interim,
               'previous_revenue_per_interim': previous_revenue_per_interim,
               'previous_customers_per_interim': previous_customers_per_interim,
               'barber_productivity': barber_productivity,
               'reviews_info': reviews_info, 'current_reviews': len(current_reviews),
               'current_average_rating': current_average_rating, 'max_load_hours': max_load_hours,
               "max_load_per_interim": max_load_per_interim, 'all_barbers': all_barbers
               }
    context.update(interim)
    return render(request, "statistica/stats.html", context)
