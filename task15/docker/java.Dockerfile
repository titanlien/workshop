# syntax=docker/dockerfile:1
FROM openjdk:11.0.14.1-slim-buster AS base

COPY app/java-webserver.jar /opt

WORKDIR /opt

EXPOSE 8080

CMD ["java", "-jar", "java-webserver.jar"]
