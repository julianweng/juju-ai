
# Juju AI

Juju AI is a simple bot made with rasa.

## Setup
Pull a docker image and start a container.
```
docker run -d -p 5005:5005 -p 5002:5002 -p 80:80 -p 8888:8888 --name rasa -e GRANT_SUDO=yes --user root -e JUPYTER_ENABLE_LAB=yes -v %cd%:/home/jovyan cliffweng/cory
```
Run these commands in the docker container
```
git clone https://github.com/julianweng/juju-ai.git
cd juju-ai
rasa train
rasa run actions &
rasa x
```