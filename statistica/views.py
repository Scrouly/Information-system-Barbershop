import datetime
from django.shortcuts import render, get_object_or_404

from reviews.models import Review
from salon.models import Barbershop
from services.models import Booking, WorkingTime
from users.models import Barber
from .utils import revenue_and_customers, difference, graph, dict_for_pie, back_dates, daily_graph


# def stats_info(request, pk, barber_pk=None):
#     print('-------------stats_info_in-------------')
#     if 'week' in request.get_full_path():
#         print('week stats')
#         print('week stats')
#         print('week stats')
#         print('week stats')
#         print('week stats')
#         print(f"request.get_full_path()---{request.get_full_path()}")
#     today = datetime.date.today()
#     barbershop = get_object_or_404(Barbershop, pk=pk)
#     barber = Barber.objects.filter(pk=barber_pk, barbershop_id=pk).first()
#
#     if barber_pk:
#         today_appointments = Booking.objects.filter(appointment_date=today, barbershop_id=pk, barber_id=barber_pk)
#         yesterday_appointments = Booking.objects.filter(appointment_date=(today - datetime.timedelta(days=1)),
#                                                         barbershop_id=pk, barber_id=barber_pk)
#     else:
#         today_appointments = Booking.objects.filter(appointment_date=today, barbershop_id=pk)
#         yesterday_appointments = Booking.objects.filter(appointment_date=(today - datetime.timedelta(days=1)),
#                                                         barbershop_id=pk)
#
#     get_barbers = [app.barber.username for app in today_appointments]
#     barber_productivity = dict_for_pie(get_barbers)
#
#     today_reviews = [rating.rating for rating in Review.objects.filter(appointment__in=today_appointments)]
#
#     reviews_info = dict(sorted(dict_for_pie(today_reviews).items(), key=lambda x: float(x[0])))
#
#     print(reviews_info)
#     print('---------------')
#     print(barber_productivity)
#
#     print([app.barber.username for app in today_appointments])
#
#     time = WorkingTime.objects.all()
#
#     try:
#         today_average_rating = round(sum(today_reviews) / len(today_reviews), 2)
#     except ZeroDivisionError:
#         today_average_rating = 0
#     print(today_average_rating)
#
#     today_revenue, today_customers = revenue_and_customers(today_appointments)
#     yesterday_revenue, yesterday_customers = revenue_and_customers(yesterday_appointments)
#
#     appointments_difference = difference(today_appointments.count(), yesterday_appointments.count())
#     customers_difference = difference(today_customers, yesterday_customers)
#     revenue_difference = difference(today_revenue, yesterday_revenue)
#
#     time = [times.hour.strftime("%H:%M") for times in time]
#
#     today_appointments_per_hour, today_revenue_per_hour, today_customers_per_hour = graph(today_appointments, time)
#     yesterday_appointments_per_hour, yesterday_revenue_per_hour, yesterday_customers_per_hour = graph(
#         yesterday_appointments, time)
#
#     context = {'barber': barber, 'barbershop': barbershop, 'today_appointments': len(today_appointments),
#                'today_revenue': today_revenue,
#                'today_customers': today_customers, 'appointments_difference': appointments_difference,
#                'customers_difference': customers_difference,
#                'revenue_difference': revenue_difference, 'time': time,
#
#                'today_appointments_per_hour': today_appointments_per_hour,
#                'today_revenue_per_hour': today_revenue_per_hour,
#                'today_customers_per_hour': today_customers_per_hour,
#
#                'yesterday_appointments_per_hour': yesterday_appointments_per_hour,
#                'yesterday_revenue_per_hour': yesterday_revenue_per_hour,
#                'yesterday_customers_per_hour': yesterday_customers_per_hour, 'barber_productivity': barber_productivity,
#                'reviews_info': reviews_info, 'today_reviews': len(today_reviews),
#                'today_average_rating': today_average_rating
#                }
#     return render(request, "statistica/stats.html", context)
#
#
# def week_stats_info(request, pk, barber_pk=None):
#     print('-------------week_stats_info-------------')
#     if 'week' in request.get_full_path():
#         print('week stats')
#         print(f"request.get_full_path()---{request.get_full_path()}")
#     today = datetime.date.today()
#     last_week = today - datetime.timedelta(days=7)
#     previous_week = last_week - datetime.timedelta(days=7)
#
#     this_week_all_dates = back_dates(today, last_week)
#     previous_week_all_dates = back_dates(last_week, previous_week)
#
#     barbershop = get_object_or_404(Barbershop, pk=pk)
#     barber = Barber.objects.filter(pk=barber_pk, barbershop_id=pk).first()
#
#     if barber_pk:
#         week_appointments = Booking.objects.filter(appointment_date__in=this_week_all_dates, barbershop_id=pk,
#                                                    barber_id=barber_pk)
#         previous_week_appointments = Booking.objects.filter(appointment_date__in=previous_week_all_dates,
#                                                             barbershop_id=pk, barber_id=barber_pk)
#     else:
#         week_appointments = Booking.objects.filter(appointment_date__in=this_week_all_dates, barbershop_id=pk,
#                                                    )
#         previous_week_appointments = Booking.objects.filter(appointment_date__in=previous_week_all_dates,
#                                                             barbershop_id=pk)
#     week_appointments = [daily_appointments for daily_appointments in week_appointments]
#     previous_week_appointments = [daily_appointments for daily_appointments in previous_week_appointments]
#     print(f"week_appointments---{week_appointments}")
#     print(f"previous_week_appointments---{previous_week_appointments}")
#
#     get_barbers = [barber.barber.username for barber in week_appointments]
#     print(f'get_barbers----{get_barbers}')
#     barber_productivity = dict_for_pie(get_barbers)
#
#     today_reviews = [rating.rating for rating in Review.objects.filter(appointment__in=week_appointments)]
#
#     reviews_info = dict(sorted(dict_for_pie(today_reviews).items(), key=lambda x: float(x[0])))
#
#     print(reviews_info)
#     print('---------------')
#     print(barber_productivity)
#
#     try:
#         today_average_rating = round(sum(today_reviews) / len(today_reviews), 2)
#     except ZeroDivisionError:
#         today_average_rating = 0
#     print(today_average_rating)
#
#     today_revenue, today_customers = revenue_and_customers(week_appointments)
#     yesterday_revenue, yesterday_customers = revenue_and_customers(previous_week_appointments)
#     print(f'today_revenue---{today_revenue}---today_customers---{today_customers}')
#     appointments_difference = difference(len(week_appointments), len(previous_week_appointments))
#     customers_difference = difference(today_customers, yesterday_customers)
#     revenue_difference = difference(today_revenue, yesterday_revenue)
#     print(
#         f'appointments_difference---{appointments_difference}---customers_difference---{customers_difference}---revenue_difference---{revenue_difference}')
#
#     today_appointments_per_hour, today_revenue_per_hour, today_customers_per_hour = daily_graph(week_appointments,
#                                                                                                 this_week_all_dates)
#     yesterday_appointments_per_hour, yesterday_revenue_per_hour, yesterday_customers_per_hour = daily_graph(
#         previous_week_appointments, previous_week_all_dates)
#
#     context = {'barber': barber, 'barbershop': barbershop, 'today_appointments': len(week_appointments),
#                'today_revenue': today_revenue,
#                'today_customers': today_customers, 'appointments_difference': appointments_difference,
#                'customers_difference': customers_difference,
#                'revenue_difference': revenue_difference, 'time': this_week_all_dates,
#
#                'today_appointments_per_hour': today_appointments_per_hour,
#                'today_revenue_per_hour': today_revenue_per_hour,
#                'today_customers_per_hour': today_customers_per_hour,
#
#                'yesterday_appointments_per_hour': yesterday_appointments_per_hour,
#                'yesterday_revenue_per_hour': yesterday_revenue_per_hour,
#                'yesterday_customers_per_hour': yesterday_customers_per_hour, 'barber_productivity': barber_productivity,
#                'reviews_info': reviews_info, 'today_reviews': len(today_reviews),
#                'today_average_rating': today_average_rating
#                }
#     return render(request, "statistica/stats.html", context)
# Create your views here.

def stats_info(request, pk, barber_pk=None):
    print('-------------stats_info_in-------------')

    today = datetime.date.today()
    barbershop = get_object_or_404(Barbershop, pk=pk)
    barber = Barber.objects.filter(pk=barber_pk, barbershop_id=pk).first()
    full_path = request.get_full_path()
    interim = {'interim': "today"}
    print(full_path)
    if 'week' in full_path:
        print('week')
    if 'month' in full_path:
        print('month')

    if 'week' in full_path or 'month' in full_path:
        print('week stats')
        print('week stats')
        print('week stats')
        print('week stats')
        print('week stats')
        print(f"full_path ---{full_path}")

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

    current_reviews = [rating.rating for rating in Review.objects.filter(appointment__in=current_appointments)]

    reviews_info = dict(sorted(dict_for_pie(current_reviews).items(), key=lambda x: float(x[0])))

    print(reviews_info)
    print('---------------')
    print(barber_productivity)

    print([app.barber.user.username for app in current_appointments])

    time = WorkingTime.objects.all()

    try:
        current_average_rating = round(sum(current_reviews) / len(current_reviews), 2)
    except ZeroDivisionError:
        current_average_rating = 0
    print(current_average_rating)

    current_revenue, current_customers = revenue_and_customers(current_appointments)
    previous_revenue, previous_customers = revenue_and_customers(previous_appointments)

    appointments_difference = difference(len(current_appointments), len(previous_appointments))
    customers_difference = difference(current_customers, previous_customers)
    revenue_difference = difference(current_revenue, previous_revenue)

    max_load_hours = [times.hour.strftime("%H:%M") for times in time]
    print(f"current_appointments---{current_appointments}")
    print(f'max_load_hours---{max_load_hours}')
    max_load_per_interim = graph(
        current_appointments,
        max_load_hours)[0]
    print(f"current_appointments_per_interim---{max_load_per_interim}")

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
               "max_load_per_interim": max_load_per_interim
               }
    context.update(interim)
    return render(request, "statistica/stats.html", context)
