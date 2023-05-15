from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from reviews.forms import ReviewForm
from reviews.models import Review
from services.models import Booking
from users.models import Barber


# def review(request, barber_pk):
#     service = Booking.objects.get(customer__pk=request.user.id, barber__pk=barber_pk)
#     print(service)
#     url = request.META.get('HTTP_REFERER')
#     if request.method == "POST":
#         try:
#             reviews = Review.objects.get(user__pk=request.user.id, barber__pk=barber_pk)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, 'Thank you! Your review has been updated.')
#             return redirect(url)
#         except Review.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = Review()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.barber_id = barber_pk
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, 'Thank you! Your review has been submitted.')
#                 return redirect(url)
#     else:
#         try:
#             # ---get_object_or_404()---
#             reviews = Review.objects.get(user__pk=request.user.id, barber__pk=barber_pk)
#             form = ReviewForm(instance=reviews)
#         except Review.DoesNotExist:
#             reviews = None
#             form = ReviewForm()
#             # -------------------------
#     content = {"user": request.user, "form": form, 'review': reviews}
#     return render(request, 'reviews/review.html', content)
def review(request, pk):
    booking = get_object_or_404(Booking, customer__pk=request.user.id, pk=pk)
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = Review.objects.get(user__pk=request.user.id, appointment__pk=booking.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect('users:profile')
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.appointment = booking
                data.barber_id = booking.barber_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect("users:profile")
    else:
        try:
            # ---get_object_or_404()---
            reviews = Review.objects.get(user__pk=request.user.id, appointment__pk=booking.id)
            form = ReviewForm(instance=reviews)
        except Review.DoesNotExist:
            reviews = None
            form = ReviewForm()
            # -------------------------
    content = {"user": request.user, "form": form, 'review': reviews, 'booking': booking}
    return render(request, 'reviews/review.html', content)


def delete_review(request, pk):
    get_review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        get_review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('users:profile')
    return render(request, 'reviews/delete_review.html', {'review': get_review})


def barber_reviews(request, pk):
    barber = get_object_or_404(Barber, pk=pk)
    reviews = Review.objects.filter(barber=barber)
    date_filter = request.GET.get('date')
    sorted_filter = request.GET.get('sorted')
    if sorted_filter == 'up':
        reviews = reviews.order_by('rating')
    elif sorted_filter == 'down':
        reviews = reviews.order_by('-rating')
    if date_filter == 'up':
        reviews = reviews.order_by('updated_time')
    elif date_filter == 'down':
        reviews = reviews.order_by('-updated_time')
    context = {"barber": barber, "reviews": reviews}
    return render(request, 'reviews/barber_reviews.html', context)
# Create your views here.
