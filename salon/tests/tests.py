import pytest
from django.urls import reverse
from django.test import RequestFactory
from users.models import CustomUser
from salon.views import index, detail_view, page_not_found
from reviews.models import Review
from salon.models import Barbershop, City
from services.models import WorkingTime


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def working_time(db):
    return WorkingTime.objects.create(hour='10:00:00')


@pytest.fixture
def user():
    return CustomUser.objects.create(username='testuser', password='testpassword')


@pytest.fixture
def city():
    return City.objects.create(name='City')


@pytest.fixture
def barbershop(city):
    return Barbershop.objects.create(
        name='Barbershop',
        short_description='Short description',
        full_description='Full description',
        phone_number='+123456789',
        email='test@example.com',
        main_photo='salon/photos/2023/01/01/photo.jpg',
        city=city,
        address='Address'
    )


@pytest.fixture
def review(user, barbershop):
    return Review.objects.create(
        user=user,
        barber=barbershop,
        subject='Review subject',
        review='Review text',
        rating=4.5
    )


@pytest.fixture
def working_time():
    return WorkingTime.objects.create(hour='10:00:00')


@pytest.mark.django_db
def test_index_view(factory, city):
    url = reverse('index')
    request = factory.get(url)
    request.GET = {'city': city.name, 'sorted': 'up'}
    response = index(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view(factory, client, barbershop, working_time):
    url = reverse('detail', args=[barbershop.pk])
    request = factory.get(url)
    request.GET = {'date': 'up', 'sorted': 'down'}
    response = detail_view(request, pk=barbershop.pk)
    assert response.status_code == 200


def test_page_not_found_view(factory):
    url = '/non-existent-url/'
    request = factory.get(url)
    response = page_not_found(request, exception=None)
    assert response.status_code == 404
