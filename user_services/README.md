<!-- ABOUT THE PROJECT -->

## User-Services Micro service

Hosts the user authentication platform and the related REST API

### Built With

- [ExpressJs]()
- [MongoDb]()

## To Get started locally

`$ npm i` <br>

Create a .env file and add neccessary DB env vars neccesary and then

`$ npm run start` <br>

to run the service <br>

## To get started with container

`$ docker-compose up --build`

## To reflect the changes in the container

`$ docker-compose down -v && docker-compose up --build`
