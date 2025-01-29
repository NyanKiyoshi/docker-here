# The arguments to pass to docker-here.sh
#
# Note: --privileged is required to run containers inside containers.
docker_here_args=--privileged --src ../ --dest /app -- python:3.12-slim sh -uxc

# The commands to run to bootstrap the python test image.
install_commands=\
        apt-get update \
        && apt-get install -y podman \
        && pip install poetry \
        && cd ./tests \
        && poetry install --with dev

.PHONY: test

test:
	../docker-here $(docker_here_args) \
		'$(install_commands) && poetry run pytest ./'

shell:
	../docker-here $(docker_here_args) \
		$(install_commands) \
		&& bash -i'

