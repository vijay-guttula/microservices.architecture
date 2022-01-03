from django.urls import path
from .views import *

urlpatterns = [
    path('books/new', NewContentsView.as_view({
      'get':'list'
    })),
    path('books', BooksViewSet.as_view({
      'get':'list',
      'post':'create', 
    })),
    path('books/<str:pk>', BooksViewSet.as_view({
      'get':'retrieve',
      'put':'update',
      'delete':'destroy', 
    })),
    
]
