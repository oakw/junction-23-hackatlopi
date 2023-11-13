# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM node:21 AS development

RUN mkdir /project
WORKDIR /project

COPY . .

RUN npm install

CMD ["npm", "run", "dev-p"]