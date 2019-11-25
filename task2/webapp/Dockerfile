FROM openjdk:8-jre-alpine

RUN wget https://s3.eu-central-1.amazonaws.com/nvplayground/demo-0.0.1-SNAPSHOT.jar -P /

EXPOSE 8080/TCP

CMD ["/usr/bin/java", "-jar", "-Dspring.profiles.active=default", "/demo-0.0.1-SNAPSHOT.jar"]
