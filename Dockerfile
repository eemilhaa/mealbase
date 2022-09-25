# FROM postgres:14-alpine
# COPY ./mealbase/schema.sql ./
FROM postgres:14
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
COPY ./mealbase/schema.sql ./
