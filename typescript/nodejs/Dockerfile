### STAGE 1: Build ###
ARG NODE_IMAGE_TAG=alpine
FROM node:${NODE_IMAGE_TAG} as build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

### STAGE 2: Run ###
FROM node:${NODE_IMAGE_TAG}
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install --only=production
COPY --from=build /usr/src/app/dist ./dist
CMD ["node", "dist/main"]