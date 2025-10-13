from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    watch_list = models.ManyToManyField(User, related_name="watch_listed_movies", blank=True)
    rating = models.IntegerField(default=0)
    # Inventory field
    amount_left = models.PositiveIntegerField(default=0, help_text="Number of copies available for purchase")
    def __str__(self):
        return str(self.id) + ' - ' + self.name

    @property
    def is_in_stock(self):
        """Check if movie is still available for purchase"""
        return self.amount_left > 0

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, default = '', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #many to many field relates users to likes. you use by adding request.user or removing request.user
    likes = models.ManyToManyField(User, related_name="liked_reviews", blank=True)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

