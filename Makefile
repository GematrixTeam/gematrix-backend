.PHONY: test install

VIRTUALENV    := virtualenv
VENV 		  := .venv
LINT 		  := flake8 --ignore E501,F401

DOCKER_NAME   := gematrix/gematrix-backend
DOCKER_TAG    := $$(git rev-parse HEAD)
DOCKER_IMG    := ${DOCKER_NAME}:${DOCKER_TAG}
DOCKER_LATEST := ${DOCKER_NAME}:latest


all: lint test

venv: $(VENV)/bin/activate
	@echo "Virtualenv is configured"
	@echo "Please run \"source $(VENV)/bin/activate\" to start using it"

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || $(VIRTUALENV) -p python3 --prompt gematrix $(VENV)
	. $(VENV)/bin/activate; pip install -Ur requirements.txt
	touch $(VENV)/bin/activate

test: venv
	. $(VENV)/bin/activate; ./gematrix/manage.py test

lint: venv
	. $(VENV)/bin/activate; $(LINT) gematrix

clean:
	git clean -dfx -e .idea/


#
# Docker related tasks
#
docker_build:
	echo ${DOCKER_TAG}
	echo ${DOCKER_IMG}
	@docker build -t ${DOCKER_IMG} .
	@docker tag ${DOCKER_IMG} ${DOCKER_LATEST}

docker_push:
	@docker push ${DOCKER_NAME}

docker_login:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}

docker_all: docker_login docker_build docker_push
