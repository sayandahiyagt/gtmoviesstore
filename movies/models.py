from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class MovieRequest(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.title}"

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rationale = models.TextField(help_text="Why it should be included")
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="petitions"
    )
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return self.title

class PetitionVote(models.Model):
    petition = models.ForeignKey(
    Petition, on_delete=models.CASCADE, related_name="votes"
    )
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="petition_votes"
    )
    is_yes = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        unique_together = ("petition", "user")
        # or modern style constraint:
        # constraints = [
        # models.UniqueConstraint(fields=["petition", "user"], name="unique_vote_per_user_per_petition")
        # ]


    def __str__(self):
        return f"{self.user} → {self.petition} : {'YES' if self.is_yes else 'NO'}"