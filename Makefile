ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# code quality
all: black typehint lint

black:
	rye run isort --multi-line 3 --profile black src/ tests/
	rye run black --target-version py311 src/ tests/

typehint: 
	rye run mypy --ignore-missing-imports src/ tests/

lint:
	rye run pylint src/

# test
test:
	rye run coverage run -m --source=stacosys pytest tests
	rye run coverage report

# build
build:
	rye run pyinstaller stacosys.spec

# run
run:
	rye run python src/stacosys/run.py $(RUN_ARGS)