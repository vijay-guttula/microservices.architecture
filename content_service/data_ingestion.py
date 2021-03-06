import csv
# django settings setup
from django.conf import settings
import django
from content_service.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from books.models import BooksModel
from books.producer import publish

def run():
  csvfile = open('books.csv', newline='')
  read_file = csv.reader(csvfile, delimiter=',')
  print(read_file)
  count = 1 #to pass header
  for record in read_file:
    print(record, count)
    if count == 1:
      pass
    else:
      book = BooksModel.objects.create(title=record[0], story=record[1])
      publish(routing_key='user_interactions', body={
        'operation':'book_created',
        'book_id': book.id
      })
    count += 1
  

if __name__ == '__main__':
  run()