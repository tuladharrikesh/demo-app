FROM node:12

WORKDIR /home/node/app

COPY package*.json ./

RUN npm install express

COPY . .

EXPOSE 8080

CMD ["node", "server.js"]