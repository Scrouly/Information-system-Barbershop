import pytest
from django.urls import reverse
from django.test import RequestFactory
from users.views import login, register, profile, logout
from users.models import CustomUser
from mixer.backend.django import mixer

@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='testuser', password='testpassword')


@pytest.mark.django_db
def test_login_view(factory, user):
    url = reverse('users:signin')
    request = factory.get(url)
    request.user = user
    response = login(request)
    assert response.status_code == 200
    assert b'form' in response.content


@pytest.mark.django_db
def test_register_view(factory):
    url = reverse('users:signup')
    request = factory.get(url)
    response = register(request)
    assert response.status_code == 200
    assert b'form' in response.content


@pytest.mark.django_db
def test_logout_view(client):
    # Создание пользователя
    user = mixer.blend(CustomUser, username='testuser', password='testpassword')

    # Авторизация пользователя
    client.login(username='testuser', password='testpassword')

    # Запрос к представлению logout
    url = reverse('users:logout')
    response = client.get(url)
    print(response)

    # Проверка результата
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert not client.session.get('_auth_user_id')
