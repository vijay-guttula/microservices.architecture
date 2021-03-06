<!-- ABOUT THE PROJECT -->

## User-Interactions Micro service

Hosts the user interactions service, which records read or likes from the user and sends it to the content_service microservice which can sort data for new content API or top content API

## Built With

- [Flask]()
- [MySql]()

## To Get started locally

`$ pip3 install -r requirements.txt` <br>

Create a .env file and add neccessary DB env vars neccesary and then
<br>

`$ python3 manage.py db init && python3 manage.py db migrate && python3 manage.py db upgrade`
<br>

`$ python3 main.py` for the app

`$ python3 consumer.py` for the event management service

## To get started with container

`$ docker-compose up --build`

## To reflect the changes in the container

`$ docker-compose down -v && docker-compose up --build`

## Do the following in case of DB migration errors

- Delete the .dbdata folder to delete the current database

- `$ docker-compose down -v`

- `$ docker-compose up db backend --build`

Now to migrate the db and start the queue. start a new terminal and run the following commands <br>

Please run all the db commands even if the db init or migrate throws an error related to already existing.

- `$ docker-compose exec backend sh`
- `$ python manage.py db init`
- `$ python manage.py db migrate`
- `$ python manage.py db upgrade`
- `$ python consumer.py`
