from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import BooksModel, LikesReadsModel

class BooksSerializer(serializers.ModelSerializer):
  class Meta:
    model = BooksModel
    fields = '__all__'
    

class LikesReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikesReadsModel
    fields = '__all__'