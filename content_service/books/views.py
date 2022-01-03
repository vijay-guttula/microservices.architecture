from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import BooksSerializer
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class BooksViewSet(viewsets.ViewSet):
  # GET /api/v1/books
  def list(self, request): 
    books = BooksModel.objects.all()
    serializer = BooksSerializer(books, many=True)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
  
  # POST /api/v1/books
  def create(self, request): 
    serializer = BooksSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
  
  # GET /api/v1/books/<str:id>
  def retrieve(self, request, pk=None):
    try:
      book = BooksModel.objects.get(id=pk)
      serializer = BooksSerializer(book)
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    
  # UPDATE /api/v1/books/<str:id>
  def update(self, request, pk=None):
    try:
      book = BooksModel.objects.get(id=pk)
      serializer = BooksSerializer(instance=book, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
  
  # DELETE /api/v1/books/<str:id>
  def destroy(self, request, pk=None):
    try:
      book = BooksModel.objects.get(id=pk)
      book.delete()
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    return Response({'status':'success'}, status=status.HTTP_204_NO_CONTENT)
  
# GET /api/v1/books/new
class NewContentsView(viewsets.ViewSet):
  def list(self, request):
    books = BooksModel.objects.order_by('-date_time')
    serializer = BooksSerializer(books, many=True)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)

# GET /api/v1/books/top
class TopConentsView(viewsets.ViewSet):
  def list(self, request):
    pass