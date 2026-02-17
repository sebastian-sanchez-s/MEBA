from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models.surveys_models import Survey, Question, Answer
from ..forms.surveys_forms import (
        SurveyForm, QuestionForm,
        ChooseQuestionForm,
        AnswerForm,
)
from ..forms.respondents_forms import ChooseRespondentForm
from django import forms

LOGIN_URL = reverse_lazy("surveys:pollsters-login")


class SurveyDashboardView(LoginRequiredMixin, View):
    template_name = "surveys/detail.html"
    login_url = LOGIN_URL

    def get(self, request, survey_id, *args, **kwargs):
        survey = Survey.objects.get(id=survey_id)
        queryset = Question.objects.exclude(survey=survey)

        context = {
            "survey": survey,
            "question_answers": survey.get_question_answers(),
            "questions_form": ChooseQuestionForm(queryset),
        }

        return render(request, self.template_name, context=context)

    def post(self, request, survey_id, *args, **kwargs):
        survey = Survey.objects.get(id=survey_id)
        queryset = Question.objects.exclude(survey=survey)

        question_list_form = ChooseQuestionForm(queryset, request.POST)

        if question_list_form.is_valid():
            question_list = question_list_form.cleaned_data["questions"]
            survey.add_questions(question_list)

        context = {
            "survey": survey,
            "question_answers": survey.get_question_answers(),
            "questions_form": ChooseQuestionForm(queryset),
        }

        return render(request, self.template_name, context=context)


class SurveyListView(ListView):
    model = Survey
    template_name = "surveys/list.html"


class SurveyFillView(LoginRequiredMixin, View):
    template_name = "surveys/fill.html"

    def get_success_url(self):
        return reverse_lazy("surveys:survey-dashboard", 
                kwargs={"survey_id": self.survey.id})

    def get(self, request, survey_id, *args, **kwargs):
        survey = Survey.objects.get(id=survey_id)
        questions = survey.question_set.all()

        choose_respondent_form = ChooseRespondentForm()
        answer_formset_class = forms.modelformset_factory(
                Answer, AnswerForm, extra=questions.count()
        )
        answer_forms = answer_formset_class(
                initial=[{"question": question} for question in questions]
        )

        for answer_form, question in zip(answer_forms, questions):
            answer_form.fields["question"].widget = forms.HiddenInput(attrs={"value": question})
            answer_form.fields["question"].label = question.question_text
            match question.answer_type:
                case 0:
                    widget = forms.TextInput()
                case 1:
                    widget = forms.NumberInput(attrs={"value": 0})
                case 2:
                    widget = forms.DateInput()
                case 3:
                    widget = forms.CheckboxInput(attrs={"checked": ""})
                case _:
                    raise ValueError("Question attribute `answer_type` is invalid.")
            answer_form.fields["answer_text"].widget = widget

        return render(request, self.template_name, context={
            "survey": survey,
            "choose_respondent_form": choose_respondent_form,
            "answer_forms": answer_forms,
        })

    def post(self, request, survey_id, *args, **kwargs):
        self.survey = Survey.objects.get(id=survey_id)
        self.questions = self.survey.question_set.all()
        self.request = request

        choose_respondent_form = ChooseRespondentForm(request.POST)

        if choose_respondent_form.is_valid():
            self.respondent = choose_respondent_form.cleaned_data.get("respondent")

            answer_formset_class = forms.modelformset_factory(
                    Answer, AnswerForm, extra=self.questions.count())
            answer_formset = answer_formset_class(
                    request.POST,
                    initial=[{"question": question} for question in self.questions]
            )

            if answer_formset.is_valid():
                return self.answer_formset_valid(answer_formset)

    def answer_formset_valid(self, formset):
        answers = formset.save(commit=False)

        for answer in answers:
            answer.survey = self.survey
            answer.pollster = self.request.user.pollster
            answer.respondent = self.respondent
            answer.save()

        return HttpResponseRedirect(self.get_success_url())


class SurveyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = "surveys/create.html"
    login_url = LOGIN_URL
    permission_required = "is_manager"

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.pollster.has_perms(perms)

    def get_success_url(self):
        return reverse_lazy("surveys:survey-list")

    def form_valid(self, form):
        user = self.request.user
        date_of_creation = timezone.now()

        survey = form.save(commit=False)

        survey.created_by = user.pollster
        survey.date_of_creation = date_of_creation

        survey.save()

        return super().form_valid(form)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "questions/list.html"


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "questions/create.html"
    login_url = LOGIN_URL

    def get_success_url(self):
        return reverse_lazy("surveys:survey-list")
