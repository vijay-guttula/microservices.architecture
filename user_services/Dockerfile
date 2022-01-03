FROM node:16.13.1
ENV PORT 3000

WORKDIR /app

COPY package.json /app/

RUN npm install

COPY . /app/

EXPOSE 3000
CMD npm start