from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from reviews.models import Review
from services.models import Booking
from users.forms import CustomUserCreationForm, CustomUserAuthentificationForm, CustomUserProfileForm
from users.models import CustomUser


# Create your views here.


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('signin')
#     template_name = 'users/signup.html'
#
#     def post(self, request, *args, **kwargs):
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#         context = {'form': form}
#         return render(request, self.template_name, context)


# class SignInView(LoginView):
#     form_class = CustomUserAuthentificationForm
#     success_url = reverse_lazy('')
#     template_name = 'users/signin.html'
#
#     def post(self, request, *args, **kwargs):
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#         context = {'form': form}
#         return render(request, self.template_name, context)

def login(request):
    print(request.GET)
    print(request.POST)
    if request.method == "POST":
        form = CustomUserAuthentificationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = CustomUserAuthentificationForm()
    context = {'form': form}
    return render(request, 'users/signin.html', context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            return HttpResponseRedirect(reverse('users:signin'))

    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)


@login_required()
def profile(request):
    get_appointments = Booking.objects.filter(customer=request.user)
    [appointment.save() for appointment in get_appointments]
    get_completed_appointments = get_appointments.filter(completed=True).order_by('-appointment_date',
                                                                                  '-appointment_time')
    get_last_appointment = get_completed_appointments.first()
    print(get_last_appointment)
    get_appointments = get_appointments.filter(completed=False).order_by('appointment_date', 'appointment_time')
    print(get_appointments)
    get_reviews = Review.objects.filter(user=request.user)
    get_booking_reviews = [review.appointment for review in get_reviews]
    print([review.appointment for review in get_reviews])
    print(f"--birth_data--{request.user.birth_data}")
    if request.method == "POST":
        form = CustomUserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        print(f"--birth_data--{request.user.birth_data}")
        print(form.errors)
        if form.is_valid():
            print(form.data)
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            if form.errors['phone_number']:
                messages.error(request, form.errors['phone_number'])
            else:
                messages.error(request, form.errors)
    else:
        request.user.birth_data = request.user.birth_data.strftime('%Y-%m-%d') if request.user.birth_data else None
        print(f"GET--birth_data--{request.user.birth_data}")
        form = CustomUserProfileForm(instance=request.user)
    context = {'form': form, "appointments": get_appointments, 'completed_appointments': get_completed_appointments,
               "last_appointment": get_last_appointment, "reviews": get_booking_reviews}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
