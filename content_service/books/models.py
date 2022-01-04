from django.db import models
from django.utils import timezone

# Create your models here.  
class UsersModel(models.Model):
  email_id = models.CharField(max_length=100, unique=True)
  
class BooksModel(models.Model):
  title = models.CharField(max_length=100, unique=True)
  story = models.CharField(max_length=500)
  date_time = models.DateTimeField(default=timezone.localtime)
  


class LikesReadsModel(models.Model):
  user_id = models.ForeignKey('UsersModel', on_delete=models.CASCADE)
  book_id = models.ForeignKey('BooksModel', on_delete=models.CASCADE)
  like = models.BooleanField(default=False)
  read = models.BooleanField(default=False)