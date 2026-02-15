from django import forms
from ..models.surveys_models import Survey, Question, Answer


class ChooseQuestionForm(forms.Form):
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.none())

    def __init__(self, queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["questions"].queryset = queryset


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("question", "answer_text",)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question_text", "answer_type",)


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ("survey_name",)
