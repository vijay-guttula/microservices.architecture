from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
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
    try:
      book_serializer = BooksSerializer(data=request.data)
      book_serializer.is_valid(raise_exception=True)
      book_serializer.save()
      
      publish(routing_key='user_interactions', body={
          'operation':'book_created',
          'book_id': book_serializer.data['id']
        })
      
      return Response({'status':'success', 'data': book_serializer.data}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      print(e)
      return Response({'status':'failure', 'message':'error processing the request \n message: {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
  
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
    try:
      books = BooksModel.objects.order_by('-date_published')
      serializer = BooksSerializer(books, many=True)
      return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response({'status':'failure', 'message':'error processing the request \n message: {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

# GET /api/v1/books/top
class TopConentsView(viewsets.ViewSet):
  def list(self, request):
    try:
      user_id = request.GET.get('user_id')
      books = LikesReadsModel.objects.filter(user_id=user_id).order_by('-like', '-read')
      serializer = LikesReadSerializer(books, many=True)
      return Response({'status':'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response({'status':'failure', 'message':'error processing the request \n message: {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)