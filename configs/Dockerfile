FROM debian:bookworm-slim

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install git -y
RUN apt-get install mariadb-client -y
COPY ./my.cnf /root/.my.cnf
# RUN pip3 install -r requirements.txt

# CMD pip3 install -r /app/requirements.txt && while : ; do sleep 1000; done
CMD while : ; do sleep 1000; done