# Launch haruna from docker container

## Install docker and docker compose plugin

Follow tutorials below:

[Install Docker Engine for Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

[Install Compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Build a docker image and create a docker container

(Optional) Build a docker image:

```bash
cd {HARUNA_DIRECTORY}/docker
docker compose build
```

Create a docker container and start it, then the main nodes of Haruna will be launched:

```bash
docker compose up
```

