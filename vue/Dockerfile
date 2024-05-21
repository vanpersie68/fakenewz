FROM node:16.18.0 AS build
WORKDIR /frontend
COPY frontend .
ENV VUE_APP_SERVER http://111.231.14.233/api/

RUN npm config set registry https://registry.npmjs.org/

FROM nginx:latest
COPY ./vue/nginx.conf /etc/nginx/conf.d/cs371.conf
COPY --from=build /frontend/dist /usr/share/nginx/html