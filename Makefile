ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: all build run test

# code quality
all: black typehint lint

black:
	uv run isort --multi-line 3 --profile black src/ tests/
	uv run black --target-version py311 src/ tests/

typehint: 
	uv run mypy --ignore-missing-imports src/ tests/

lint:
	uv run pylint src/

# check
check: all

# test
test:
	PYTHONPATH=src/ uv run coverage run -m --source=stacosys pytest tests
	uv run coverage report

# build
build:
	uv build --wheel --out-dir dist
	docker build -t kianby/stacosys .

# run
run:
	PYTHONPATH=src/ uv run python src/stacosys/run.py $(RUN_ARGS)