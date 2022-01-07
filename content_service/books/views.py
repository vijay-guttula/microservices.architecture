from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from books.producer import publish
from .serializers import BooksSerializer, LikesReadSerializer
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class BooksViewSet(viewsets.ViewSet):
  # GET /api/v1/books?id
  def retrieve(self, request):
    try:
      id = request.GET.get('id')
      if id is None:
        books = BooksModel.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
      
      book = BooksModel.objects.get(id=id)
      serializer = BooksSerializer(book)
      
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
  
  # POST /api/v1/books
  def create(self, request): 
    book_serializer = BooksSerializer(data=request.data)
    book_serializer.is_valid(raise_exception=True)
    book_serializer.save()
    
    publish(routing_key='user_interactions', body={
        'operation':'book_created',
        'book_id': book_serializer.data['id']
      })
    
    return Response({'status':'success', 'data': book_serializer.data}, status=status.HTTP_201_CREATED)
  
  # UPDATE /api/v1/books?id
  def update(self, request):
    try:
      id = request.GET.get('id')
      book = BooksModel.objects.get(id=id)
      serializer = BooksSerializer(instance=book, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
  
  # DELETE /api/v1/books?id
  def destroy(self, request):
    try:
      id = request.GET.get('id')
      book = BooksModel.objects.get(id=id)
      book.delete()
    except ObjectDoesNotExist:
      return Response({'status':'failure', 'data':'book does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    publish(routing_key='user_interactions', body={
        'operation':'book_deleted',
        'book_id': id
      })
    
    return Response({'status':'success'}, status=status.HTTP_204_NO_CONTENT)
  
# GET /api/v1/books/new
class NewContentsView(viewsets.ViewSet):
  def list(self, request):
    books = BooksModel.objects.order_by('-date_time')
    serializer = BooksSerializer(books, many=True)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)

# POST /api/v1/books/likes-reads
class LikesOrReadsView(APIView):
  def post(self, request):
    try:
      # user = UsersModel(id='1')
      # book = BooksModel
      book = LikesReadsModel.objects.get(book_id='14', user_id='1')
      likesreads_serializer = LikesReadSerializer(instance=book,data=request.data)
      
      return Response({'status':'success', 'data': likesreads_serializer.data}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
      likesreads_serializer = LikesReadSerializer(data=request.data)
      likesreads_serializer.is_valid(raise_exception=True)
      likesreads_serializer.save()
      
      return Response({'status':'success', 'data': likesreads_serializer.data}, status=status.HTTP_200_OK)
    

# GET /api/v1/books/top
class TopConentsView(viewsets.ViewSet):
  def list(self, request):
    user_id = request.GET.get('user_id')
    books = LikesReadsModel.objects.filter(user_id=user_id).order_by('-like')
    serializer = LikesReadSerializer(books, many=True)
    
    return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)