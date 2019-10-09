FROM node:lts-jessie

# Create app directory
WORKDIR /root/app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 8080
ENTRYPOINT ["npm", "start"]