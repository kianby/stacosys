all: black test typehint lint 

black:
	poetry run isort --multi-line 3 --profile black stacosys/
	poetry run black stacosys/

test:
	poetry run pytest

typehint: 
	poetry run mypy --ignore-missing-imports stacosys/

lint:
	poetry run pylint stacosys/

