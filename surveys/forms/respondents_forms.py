from django import forms
from ..models.respondents_models import Respondent


class RespondentForm(forms.ModelForm):
    class Meta:
        model = Respondent
        fields = (
                "fname_1", "fname_2",
                "lname_1", "lname_2",
                "date_of_birth",
        )
        widgets = {
                "date_of_birth": forms.DateInput(attrs={'type': 'date'}),
        }


class ChooseRespondentForm(forms.Form):
    respondent = forms.ModelChoiceField(queryset=Respondent.objects.all())
