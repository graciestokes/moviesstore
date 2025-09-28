from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #many to many field relates users to upvotes. you use by adding request.user or removing request.user
    upvotes = models.ManyToManyField(User, related_name="upvoted_petitions", blank=True)

    def __str__(self):
        return str(self.id)