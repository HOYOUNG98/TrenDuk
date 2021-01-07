FROM node

WORKDIR /usr/app

COPY package*.json ./

RUN npm install -g serve

COPY . .

RUN npm run build
COPY .env ./build/
WORKDIR ./build/

EXPOSE 80
CMD serve -s build

