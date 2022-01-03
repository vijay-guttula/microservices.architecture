from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import BooksModel

class BooksSerializer(serializers.ModelSerializer):
  class Meta:
    model = BooksModel
    fields = '__all__'