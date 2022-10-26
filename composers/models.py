from django.contrib.auth.models import AbstractUser
from django.db import models


class Epoch(models.Model):
    epoch = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.epoch}"


class Genre(models.Model):
    genre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.genre}"


class Composer(models.Model):
    composer_id = models.IntegerField()
    name = models.CharField(max_length=255)
    complete_name = models.CharField(max_length=255)
    epoch = models.ForeignKey(Epoch, on_delete=models.CASCADE, null=True, related_name="epoch_composers")
    birth = models.DateField()
    death = models.DateField(blank=True, null=True)
    portrait = models.URLField(blank=True, null=True)
    is_popular = models.BooleanField(blank=True, null=True)
    is_recommended = models.BooleanField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="genre_composers")

    def __str__(self):
        return f"{self.composer_id}: {self.complete_name}"


class Work(models.Model):
    title = models.CharField(max_length=255)
    is_popular = models.BooleanField(blank=True, null=True)
    is_recommended = models.BooleanField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, related_name="genre_works")
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, null=True, related_name="composer_works")
    liked_date_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.composer.complete_name}: {self.title} - {self.genre}"


class User(AbstractUser, models.Model):
    favorites = models.ManyToManyField(Work, blank="true", related_name="liked_by")


class Like(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="all_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_likes")
    liked_date_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.work}"