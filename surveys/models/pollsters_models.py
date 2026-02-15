from django.db import models
from Survey import settings

'''

Pollster <1---1> (auth) User

'''


class Pollster(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def has_perm(self, perm):
        return self.user.has_perm(perm)

    def has_perms(self, perms):
        if 'is_manager' in perms:
            return self.is_manager
        return False
