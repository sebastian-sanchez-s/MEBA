from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.respondents_models import Respondent
from ..forms.respondents_forms import RespondentForm

LOGIN_URL = reverse_lazy("surveys:pollsters-login")
POLLSTERS_DASHBOARD = reverse_lazy("surveys:pollsters-dashboard")


class RespondentListView(LoginRequiredMixin, ListView):
    model = Respondent
    template_name = "respondents/list.html"


class RespondentCreateView(LoginRequiredMixin, CreateView):
    model = Respondent
    form_class = RespondentForm
    template_name = "respondents/register.html"
    login_url = LOGIN_URL

    def get_success_url(self):
        return POLLSTERS_DASHBOARD
