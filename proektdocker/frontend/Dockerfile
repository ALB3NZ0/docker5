FROM node:alpine

WORKDIR /docker-project

COPY package*.json ./

RUN npm install

COPY . . 

EXPOSE 3000

CMD [ "npm", "start"]