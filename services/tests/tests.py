import pytest
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.test import RequestFactory
from django.test import Client
from datetime import datetime
from salon.models import Barbershop
from services.forms import BookingForm
from services.models import ServicePrice, Qualifications, WorkingTime, Booking
from services.views import booking_success, booking, barber as barber_view, service as service_view, delete_booking
from users.models import CustomUser, Barber
from django.contrib.messages import get_messages


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user():
    return mixer.blend(CustomUser, username='testuser', password='testpassword')


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def custom_user():
    return mixer.blend(CustomUser)


@pytest.fixture
def barbershop():
    return mixer.blend(Barbershop)


@pytest.fixture
def qualification():
    return mixer.blend(Qualifications)


@pytest.fixture
def barber(qualification, barbershop):
    return mixer.blend(Barber, barbershop=barbershop, qualification=qualification)


@pytest.fixture
def service_price(barber):
    return mixer.blend(ServicePrice, qualification=barber.qualification)


@pytest.fixture
def booking_form():
    return BookingForm()


@pytest.fixture
def working_time():
    return mixer.blend(WorkingTime, hour="23:00:00")


@pytest.mark.django_db
def test_booking_success_view(request_factory, user):
    url = reverse('services:success')
    request = request_factory.get(url)
    request.user = user
    response = booking_success(request)
    assert response.status_code == 200
    assert 'booking' in response.content.decode()


@pytest.mark.django_db
def test_booking_view_get(request_factory, client, user, custom_user, barbershop, barber, service_price, booking_form,
                          working_time):
    url = reverse('services:booking')
    request = request_factory.get(url,
                                  {'barbershop': barbershop.pk, 'barber': barber.pk, 'service': service_price.pk,
                                   'appointment': f'{datetime.now().date()}-23:00'})
    request.user = user
    response = booking(request)
    print(response)
    assert response.status_code == 200
    assert 'barbershop' in response.content.decode()
    assert 'barber' in response.content.decode()
    assert 'service' in response.content.decode()
    assert 'appointment' in response.content.decode()
    assert 'form' in response.content.decode()


@pytest.mark.django_db
def test_barber_view(request_factory, barbershop, barber, service_price, user, working_time):
    url = reverse('services:barbers')
    request = request_factory.get(url,
                                  {'barbershop': barbershop.pk, 'barber': barber.pk, 'service': service_price.pk,
                                   'appointment': f'{datetime.now().date()}-23:00'})
    request.user = user
    response = barber_view(request)

    # Проверка статуса ответа и контекста
    assert response.status_code == 200
    assert barber.qualification.name in response.content.decode()
    assert barber.user.first_name in response.content.decode()


@pytest.mark.django_db
def test_service_view(request_factory, barbershop, barber, service_price, user, working_time):
    # Подготовка URL-адреса для вызова представления
    url = reverse('services:services')
    # Отправка GET-запроса
    request = request_factory.get(url,
                                  {'barbershop': barbershop.pk, 'barber': barber.pk, 'service': service_price.pk,
                                   'appointment': f'{datetime.now().date()}-23:00'})
    request.user = user
    # Авторизация пользователя и отправка запроса в функцию
    response = service_view(request)
    # Проверка статуса ответа и контекста
    assert response.status_code == 200
    assert service_price.service.name in response.content.decode()
    assert str(service_price.price) in response.content.decode()


@pytest.mark.django_db
def test_delete_booking_view(request_factory, client, user, working_time):
    # Создание тестового объектов с помощью mixer
    rand_booking = mixer.blend(Booking, customer=user, completed=False, appointment_date=datetime.now().date(),
                               appointment_time=working_time)
    # Подготовка URL-адреса для вызова представления
    url = reverse('services:delete_booking', args=[rand_booking.pk])
    # Авторизация пользователя
    client.force_login(user)
    # Отправка GET-запроса
    response = client.get(url)
    # Проверка статуса ответа
    assert response.status_code == 200
    # Отправка POST-запроса для удаления записи
    response = client.post(url)
    # Проверка статуса ответа и редиректа
    assert response.status_code == 302
    assert response.url == reverse('users:profile')
    # Проверка удаления записи
    assert not Booking.objects.filter(pk=rand_booking.pk).exists()
    # Проверка сообщения об успешном удалении записи
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Запись была отменена'


@pytest.mark.django_db
def test_appointment_view(client, barbershop, barber, service_price, user):
    # Подготовка URL-адреса для вызова представления
    url = reverse('services:appointment')
    # Авторизация пользователя
    client.force_login(user)
    # Отправка GET-запроса с параметрами
    response = client.get(url, {'barbershop': barbershop.id, 'barber': barber.id, 'service': service_price.id})
    # Проверка статуса ответа и контекста
    assert response.status_code == 200
    # Проверка доступных дней и времени
    appointment = response.context['appointment']
    assert isinstance(appointment, list)
    for day in appointment:
        assert isinstance(day, dict)
        assert 'date' in day
        assert 'day' in day
        assert 'free_time' in day
