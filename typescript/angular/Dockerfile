### STAGE 1: Build ###
ARG NODE_IMAGE_TAG=alpine
FROM node:${NODE_IMAGE_TAG} as build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

### STAGE 2: Run ###
ARG NGINX_IMAGE_TAG=alpine
FROM nginx:${NGINX_IMAGE_TAG}
COPY --from=build /usr/src/app/dist/cms-webui /usr/share/nginx/html
EXPOSE 80