# Container_online

Simple Web application application to deploy docker containers and analyze performance metrics.

Uses [cadvisor](https://github.com/google/cadvisor) for visualizing performance metrics.

## Usage
* Requires [docker engine](https://docs.docker.com/engine/install/debian/) to be installed
* Run [cadvisor](https://github.com/google/cadvisor) docker container
```
pip install -r requirements.txt
flask run
```

* Visit the served website.
* Upload the Dockerfile and any other required files.
* Select a container to see the performance metrics
