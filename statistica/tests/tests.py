import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from salon.models import Barbershop
from services.models import Booking
from statistica.views import stats_info
from users.models import Barber, CustomUser


@pytest.fixture
def barbershop():
    barbershop = mixer.blend(Barbershop)
    return barbershop


@pytest.fixture
def barber(barbershop):
    barber = mixer.blend(Barber, barbershop=barbershop)
    return barber


@pytest.fixture
def booking(barbershop, barber):
    booking = mixer.blend(Booking, barbershop=barbershop, barber=barber)
    return booking


@pytest.fixture
def permission():
    content_type = ContentType.objects.get_for_model(Barber)
    permission = Permission.objects.get(content_type=content_type, codename='add_barber')
    return permission


@pytest.fixture
def user(permission):
    user = mixer.blend(CustomUser)
    user.user_permissions.add(permission)

    return user


@pytest.mark.django_db
def test_stats_info_view(client, barbershop, barber, booking, user):
    factory = RequestFactory()
    urls = [reverse('stats:day_stats_info', args=[barbershop.pk]),
            reverse('stats:week_stats_info', args=[barbershop.pk]),
            reverse('stats:month_stats_info', args=[barbershop.pk])]
    for url in urls:
        request = factory.get(url)
        request.user = user
        response = stats_info(request, barbershop.pk)
        assert response.status_code == 200
        response = stats_info(request, barbershop.pk, barber.pk)
        assert response.status_code == 200
        assert barber.user.username in response.content.decode()
        assert barbershop.name in response.content.decode()
