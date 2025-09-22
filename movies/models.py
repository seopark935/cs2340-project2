from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model): # controls model properties
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    amount_left = models.PositiveIntegerField(default=1) #new
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0) # new
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
