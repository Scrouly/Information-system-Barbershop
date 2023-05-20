import pytest
from django.urls import reverse
from mixer.backend.django import mixer

from reviews.models import Review
from services.models import Booking
from users.models import CustomUser, Barber


@pytest.fixture
def user():
    user = mixer.blend(CustomUser)
    return user


@pytest.fixture
def booking(user):
    booking = mixer.blend(Booking, customer=user)
    return booking


@pytest.fixture
def review(booking, user):
    review = mixer.blend(Review, appointment=booking, user=user)
    return review


@pytest.fixture
def barber(user):
    barber = mixer.blend(Barber, user=user)
    return barber


@pytest.mark.django_db
def test_review_view(client, booking, user):
    url = reverse('reviews:review', args=[booking.pk])
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, {'subject': 'Test Subject', 'rating': 5, 'review': 'Test Review'})
    assert response.status_code == 302  # Redirects after successful POST
    assert response.url == reverse('users:profile')

    # Make sure the review is saved
    review = Review.objects.get(user=user, appointment=booking)
    assert review.subject == 'Test Subject'
    assert review.rating == 5
    assert review.review == 'Test Review'


@pytest.mark.django_db
def test_delete_review_view(client, review):
    url = reverse('reviews:delete_review', args=[review.pk])

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url)
    assert response.status_code == 302  # Redirects after successful POST
    assert response.url == reverse('users:profile')

    # Make sure the review is deleted
    with pytest.raises(Review.DoesNotExist):
        Review.objects.get(pk=review.pk)


@pytest.mark.django_db
def test_barber_reviews_view(client, barber):
    url = reverse('reviews:barber_reviews', args=[barber.pk])

    response = client.get(url)
    assert response.status_code == 200

    # Add test cases for sorting and filtering if needed
