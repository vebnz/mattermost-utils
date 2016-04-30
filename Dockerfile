FROM ubuntu:latest
MAINTAINER Arvin Rimorin "rayarvin@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /opt/services/mattermost-utils/src
VOLUME ["/opt/services/mattermost-utils/src"]
WORKDIR /opt/services/mattermost-utils/src
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
EXPOSE 5000
