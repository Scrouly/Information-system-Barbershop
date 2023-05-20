import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import TestCase
from reviews.models import Review
from services.models import Booking
from users.forms import CustomUserProfileForm
from users.models import CustomUser
from users.views import profile

@pytest.mark.django_db
def test_profile_view(client):
    # Create a request object
    factory = RequestFactory()
    request = factory.get(reverse('users:profile'))
    request.user = mixer.blend(CustomUser)  # Create a dummy user

    # Call the profile view
    response = profile(request)

    # Perform assertions on the response
    assert response.status_code == 200
    response = client.post(reverse('users:profile'), data={request.user.first_name:'james'})
    # Assert the response status code
    assert response.status_code == 302

