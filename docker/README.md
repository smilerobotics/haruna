# Launch haruna from docker container

## Install docker and docker compose plugin

Follow tutorials below:

[Install Docker Engine for Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

[Install Compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Build a docker image and create a docker container

Build a docker image.
It would take 1200 seconds:

```bash
cd {HARUNA_DIRECTORY}/docker
docker compose build
```

Create a docker container and start it in background:

```bash
docker compose up -d
```

## Launch haruna

Attach to the docker container created by docker-compose:

```bash
docker compose exec haruna /bin/bash
```

Set up haruna:

```bash
source /root/catkin_ws/devel/setup.bash
```

Then you can use `roslaunch` command to launch haruna.

The description of the launch files is [here](../docs/launch.md).
