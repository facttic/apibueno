FROM node:10
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run sass
EXPOSE 3000
CMD [ "node", "app.js" ]