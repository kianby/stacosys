ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

all: black test typehint lint 

black:
	poetry run isort --multi-line 3 --profile black src/ tests/
	poetry run black --target-version py311 src/ tests/

test:	
	rye run coverage run -m --source=stacosys pytest tests
	rye run coverage report

typehint: 
	rye run mypy --ignore-missing-imports stacosys/ tests/

lint:
	rye run pylint src/

build:
	rye run pyinstaller stacosys.spec

run:
	rye run python src/stacosys/run.py $(RUN_ARGS)