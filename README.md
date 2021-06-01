# Docker Compose Recipe for Numbas LTI Tool

This repository contains a recipe to run the [Numbas LTI tool provider](https://numbas-lti-provider.readthedocs.io/en/latest/) in Docker.

It contains everything needed to run the Numbas LTI tool in Docker containers.

## Documentation

There's documentation for administrators, instructors and students at [numbas-lti-provider.readthedocs.io](https://numbas-lti-provider.readthedocs.io/).

## Installation

### Prerequisites

Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your server.

### Setup

Copy the file `settings.env.dist` to `settings.env` and write your own values each of the variables inside.

Run the get_secret_key script to generate a value for the SECRET_KEY environment variable, and put that in `settings.env`:

```
docker-compose run --rm numbas-setup python ./get_secret_key
```

Obtain an SSL certificate and key for the domain you will access the Numbas LTI provider from. Copy the key to `files/ssl/numbas-lti.key` and the certificate to `files/ssl/numbas-lti.pem`.

Run the installation script, to set up the database and create the superuser account:

```
docker-compose run --rm numbas-setup python ./install
```

The LTI provider is ready to start.

### Starting

Run the following command:

```
docker-compose up --scale daphne=4 --scale workers=4 --scale huey=2
```

You can customise the number of numbas-lti workers, daphne processes and huey process by changing the numbers in the `--scale` arguments.

### Stopping

Stop the numbas-lti containers with `docker-compose down`.

## Running in the cloud

Docker Compose files can also be used to deploy to the cloud. See the following documents for more information about deploying Docker to the cloud:
 - [Compose for Amazon ECS](https://docs.docker.com/engine/context/ecs-integration/)
 - [Compose for Microsoft ACI](https://docs.docker.com/engine/context/aci-integration/)
