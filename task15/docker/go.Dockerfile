# syntax=docker/dockerfile:1
FROM golang:1.16-alpine AS base

WORKDIR /app

COPY app/golang-webserver/go.mod ./
COPY app/golang-webserver/go.sum ./
RUN go mod download

COPY app/golang-webserver/*.go ./

RUN CGO_ENABLED=0 go build -o build/golang-webserver

FROM scratch AS deploy

COPY --from=base /app/build/golang-webserver /

EXPOSE 8080

CMD ["/golang-webserver"]
