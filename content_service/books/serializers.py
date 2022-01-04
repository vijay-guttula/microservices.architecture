from rest_framework import serializers
from .models import BooksModel, LikesReadsModel, UsersModel

class BooksSerializer(serializers.ModelSerializer):
  class Meta:
    model = BooksModel
    fields = '__all__'
    

class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = UsersModel
    fields = '__all__'

class LikesReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikesReadsModel
    fields = '__all__'