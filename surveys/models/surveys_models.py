from django.db import models
from .pollsters_models import Pollster
from .respondents_models import Respondent

'''

Survey <1----*> Question <1----1> Answer

'''


class Survey(models.Model):
    created_by = models.ForeignKey(Pollster, on_delete=models.PROTECT)
    date_of_creation = models.DateField()
    survey_name = models.CharField(max_length=80)

    def __str__(self):
        return self.survey_name

    def add_question(self, question):
        self.question_set.add(question)

    def add_questions(self, question_list):
        for question in question_list:
            self.add_question(question)

    def get_question_answers(self):
        questions = self.question_set.all()
        answers = self.answer_set.all()
        answers_list = []
        for question in questions:
            answers_list.append(answers.filter(question=question))
        return zip(questions, answers_list)


class Question(models.Model):
    QUESTION_TYPES = (#  html valid names
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "checkbox"),
    )

    question_text = models.CharField(max_length=200)
    answer_type = models.IntegerField(default=0, choices=QUESTION_TYPES)
    survey = models.ManyToManyField(Survey, default=None)

    def __str__(self):
        return f'text: {self.question_text} -- type: {self.get_answer_type_display()}'


class Answer(models.Model):
    pollster = models.ForeignKey(Pollster, on_delete=models.PROTECT)
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date_of_creation = models.DateField(auto_now_add=True)
    answer_text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.respondent or 'No respondent.'} says {self.answer_text or 'No answer.'} to {self.question or 'No question'}"
