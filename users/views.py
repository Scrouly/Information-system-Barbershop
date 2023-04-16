from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm, CustomUserAuthentificationForm


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
            return HttpResponseRedirect(reverse('users:signin'))

    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/signup.html', context)
