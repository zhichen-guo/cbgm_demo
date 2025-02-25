FROM node:23

WORKDIR /webapp
COPY package.json .
COPY package-lock.json .
RUN npm install

CMD ["npm", "run", "dev"]