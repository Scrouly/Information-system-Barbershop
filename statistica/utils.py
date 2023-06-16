import datetime


def revenue_and_customers(daily_appointments):
    revenue = sum([float(appointment.service.price) for appointment in daily_appointments])
    customers = len(set([appointment.customer.username for appointment in daily_appointments]))
    return revenue, customers


def difference(current_value, previous_value):
    try:
        discord = (current_value - previous_value) / current_value * 100
    except ZeroDivisionError:
        discord = -100
    return round(discord, 2)


def graph(daily_appointments, working_time):
    appointments_per_hour_list = []
    revenue_per_hour_list = []
    customers_per_hour_list = []
    for hour in working_time:
        temp_appointment = 0
        temp_revenue = 0
        temp_customers = []
        for meeting in daily_appointments:
            if meeting.appointment_time.hour.strftime("%H:%M") == hour:
                temp_appointment += 1
                temp_revenue += meeting.service.price
                temp_customers.append(meeting.customer.username)
        appointments_per_hour_list.append(temp_appointment)
        revenue_per_hour_list.append(float(temp_revenue))
        customers_per_hour_list.append(len(set(temp_customers)))

    return appointments_per_hour_list, revenue_per_hour_list, customers_per_hour_list


def daily_graph(daily_appointments, working_time):
    appointments_per_day_list = []
    revenue_per_day_list = []
    customers_per_day_list = []
    for day in working_time:
        temp_appointment = 0
        temp_revenue = 0
        temp_customers = []
        for meeting in daily_appointments:
            if str(meeting.appointment_date) == day:
                temp_appointment += 1
                temp_revenue += meeting.service.price
                temp_customers.append(meeting.customer.username)
        appointments_per_day_list.append(temp_appointment)
        revenue_per_day_list.append(float(temp_revenue))
        customers_per_day_list.append(len(set(temp_customers)))

    return appointments_per_day_list, revenue_per_day_list, customers_per_day_list


def dict_for_pie(obj):
    dictionary = {}
    for name in obj:
        dictionary.setdefault(name)
        dictionary[name] = obj.count(name)
    return dictionary


def back_dates(current_day, last_day):
    all_dates = []
    while current_day >= last_day:
        all_dates.append(current_day.strftime('%Y-%m-%d'))
        current_day -= datetime.timedelta(days=1)
    return all_dates
