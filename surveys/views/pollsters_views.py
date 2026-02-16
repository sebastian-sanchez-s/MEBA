from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models.pollsters_models import Pollster


@login_required(login_url=reverse_lazy("surveys:pollsters-login"))
def pollsters_dashboard_view(request):
    return render(request, "pollsters/dashboard.html")


class PollsterLoginView(LoginView):
    template_name = "pollsters/login.html"
    next_page = reverse_lazy("surveys:pollsters-dashboard")


class PollsterLogoutView(LogoutView):
    template_name = "pollsters/logout.html"
    next_page = reverse_lazy("surveys:pollsters-dashboard")


class PollsterCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "pollsters/register.html"

    def get_success_url(self):
        return reverse_lazy("surveys:pollsters-dashboard")

    def form_valid(self, form):
        user = form.save()

        Pollster.objects.create(user=user)

        login(self.request, user)

        return super().form_valid(form)
