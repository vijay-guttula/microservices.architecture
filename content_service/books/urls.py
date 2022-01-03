from django.urls import path
from .views import *

urlpatterns = [
    path('books/new', NewContentsView.as_view({
      'get':'list'
    })),
    path('books', BooksViewSet.as_view({
      'get':'list',
       
    })),
    path('book', BooksViewSet.as_view({
      'get':'retrieve',
      'post':'create',
      'put':'update',
      'delete':'destroy', 
    })),
    
]
