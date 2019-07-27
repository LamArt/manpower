from django.db import models


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=10000, null=True, blank=True)
    duty = models.TextField(max_length=10000, null=True, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    qualification = models.TextField(max_length=10000, null=True, blank=True)
    site_id = models.CharField(max_length=127, null=True, blank=True)
    employment = models.CharField(max_length=1000, null=True, blank=True)
    specialisation = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return '#{id} {name}'.format(id=self.id, name=self.id)
