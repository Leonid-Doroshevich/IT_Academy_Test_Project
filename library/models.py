from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)
    country_of_birth = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

    def clean(self):
        if self.date_of_birth and self.date_of_death:
            if self.date_of_death < self.date_of_birth:
                raise ValidationError("Дата смерти не может быть раньше даты рождения.")


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ImageField(upload_to='books/', null=True, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title
