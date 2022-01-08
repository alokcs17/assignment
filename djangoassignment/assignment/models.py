from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.BigIntegerField(unique=True, db_index=True)
    email = models.EmailField(max_length=255, db_index=True, null=True, blank=True)

    def __str__(self):
        name = self.name
        if self.phone:
            name += ", " + str(self.phone)
        return name.strip()

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)