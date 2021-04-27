## Docker Compose Recipe for Numbas LTI Tool

### Prerequisites

Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your server.

### Setup

Copy the file `settings.env.dist` to `settings.env` and write your own values each of the variables inside.

Obtain an SSL certificate and key, copy the key to `files/ssl/numbas-lti.key` and the certificate to `files/ssl/numbas-lti.pem`.

Run locally with the command `docker-compose up --scale daphne=4 --scale workers=4 --scale huey=2`.

You can customise the number of numbas-lti workers, daphne processes and huey process by changing the numbers in the `--scale` arguments.

### Stopping

Stop the numbas-lti containers with `docker-compose down`.

### Cloud

Docker Compose files can also be used to deploy to the cloud. See the following documents for more information about deploying Docker to the cloud:
 - [Compose for Amazon ECS](https://docs.docker.com/engine/context/ecs-integration/)
 - [Compose for Microsoft ACI](https://docs.docker.com/engine/context/aci-integration/)
