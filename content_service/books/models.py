from django.db import models
# from django.utils import timezone
# from adaptor.fields import DateField

# Create your models here.  
class UsersModel(models.Model):
  user_id = models.CharField(max_length=200, primary_key=True)
  email_id = models.CharField(max_length=100, unique=True)
  
class BooksModel(models.Model):
  title = models.CharField(max_length=100, unique=True)
  story = models.CharField(max_length=500)
  date_published = models.DateField(auto_now=True)
  


class LikesReadsModel(models.Model):
  like_read_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey('UsersModel', on_delete=models.CASCADE)
  book_id = models.ForeignKey('BooksModel', on_delete=models.CASCADE)
  like = models.BooleanField(default=False)
  read = models.BooleanField(default=False)
  
