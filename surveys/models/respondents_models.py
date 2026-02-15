from django.db import models
from django.utils import timezone


class Respondent(models.Model):
    fname_1 = models.CharField(max_length=100)
    fname_2 = models.CharField(max_length=100, default=None, blank=True)
    lname_1 = models.CharField(max_length=100)
    lname_2 = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.fname_1} {self.lname_1} (age: {self.age})'

    @property
    def age(self):
        return timezone.now().year - self.date_of_birth.year


