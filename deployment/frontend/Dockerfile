FROM node:16-bullseye-slim AS build
WORKDIR /app
COPY  src/magnit/magnit_app/components/frontend .
RUN npm install
RUN npm run build

FROM nginx as production
RUN mkdir /app
COPY --from=build /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf