from django.urls import path
from .views import *

urlpatterns = [
    path('books', BooksViewSet.as_view({
      'get':'retrieve',
      'post':'create',
      'put':'update',
      'delete':'destroy', 
    })),
    path('books/new', NewContentsView.as_view({
      'get':'list'
    })),
    path('books/top', TopConentsView.as_view({
      'get':'list'
    })),
    path('books/likes-reads', LikesOrReadsView.as_view()),
]
