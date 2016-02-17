from django.db import models


class PeriodManager(models.Manager):

    MIDDAY = '12:00'

    def morning(self):
        return self.filter(start__lt=self.MIDDAY)

    def afternoon(self):
        return self.filter(start__gte=self.MIDDAY)


class KindQuerySet(models.QuerySet):

    def emails(self):
        return self.filter(kind=self.model.EMAIL)

    def phones(self):
        return self.filter(kind=self.model.TELEPHONE)
