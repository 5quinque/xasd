FROM node:19 as build-stage

# build stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV NODE_ENV=production
RUN npm run build

# production stage
FROM nginx:stable as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

COPY ./config/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]