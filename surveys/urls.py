from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from .views.pollsters_views import (
        pollsters_dashboard_view, PollsterCreateView,
        PollsterLoginView, PollsterLogoutView,
)
from .views.surveys_views import (
        SurveyDashboardView, SurveyFillView,
        SurveyListView, SurveyCreateView,
        QuestionListView, QuestionCreateView,
)
from .views.respondents_views import (
        RespondentListView,
        RespondentCreateView,
)


app_name = "surveys"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("surveys:pollsters-dashboard"))),
    #
    path("surveys/", SurveyListView.as_view(), name="survey-list"),
    path("surveys/<int:survey_id>/", SurveyDashboardView.as_view(), name="survey-dashboard"),
    path("surveys/fill/<int:survey_id>/", SurveyFillView.as_view(), name="survey-fill"),
    path("surveys/create/", SurveyCreateView.as_view(), name="survey-create"),
    #
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("questions/create/", QuestionCreateView.as_view(), name="question-create"),
    # 
    path("respondents/", RespondentListView.as_view(), name="respondents-list"),
    path("respondents/register/", RespondentCreateView.as_view(), name="respondents-register"),
    #
    path("pollsters/dashboard/", pollsters_dashboard_view, name="pollsters-dashboard"),
    path("pollsters/login/", PollsterLoginView.as_view(), name="pollsters-login"),
    path("pollsters/logout/", PollsterLogoutView.as_view(), name="pollsters-logout"),
    path("pollsters/register/", PollsterCreateView.as_view(), name="pollsters-register"),
]
