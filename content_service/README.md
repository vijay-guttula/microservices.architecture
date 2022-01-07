<!-- ABOUT THE PROJECT -->

## User-Interactions Micro service

Hosts the books service data, and also retrieves data from the user service and user interactions microservices for NEW Content and TOP content APIs

## Built With

- [Django]()
- [Postgres]()

## To Get started locally

`$ pip3 install -r requirements.txt` <br>

Create a .env file and add neccessary DB env vars neccesary and then

`$ python3 manage.py makemigrations && python3 manage.py migrate` for db migrations <br>

`$ python3 manage.py wait-for-db && python3 manage.py runserver 0.0.0.0:8000` for the app <br>

`$ python3 consumer.py` for the event management service <br>

## For data ingestion through csv

Add a file named books.csv in the root folder and then run <br>

`$ python data_ingestion.py `

## To get started with container

`$ docker-compose up --build`

## To reflect the changes in the container

`$ docker-compose down -v && docker-compose up --build`

## To ingest the data inside the container

`$ docker-compose exec backend sh` <br>
`$ python data_ingestion.py`
