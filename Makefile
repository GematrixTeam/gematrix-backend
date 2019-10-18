.PHONY: test install

VIRTUALENV = virtualenv
VENV = .venv
LINT = flake8 --ignore E501,F401

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


