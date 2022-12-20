FROM node:16-bullseye-slim AS build
WORKDIR /app
COPY  ./components/frontend .
RUN npm install -g npm@9.1.3
RUN npm install
RUN npm run build

FROM nginx as production
RUN mkdir /app
COPY --from=build /app/dist /app
COPY ./.devcontainer/frontend/nginx.conf /etc/nginx/nginx.conf