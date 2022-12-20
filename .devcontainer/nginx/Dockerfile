FROM nginx as production
RUN mkdir /app
#COPY --from=build /app/dist /app
COPY ./.devcontainer/nginx/nginx.conf /etc/nginx/nginx.conf