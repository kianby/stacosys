all: black test typehint lint 

black:
	poetry run isort --multi-line 3 --profile black stacosys/ tests/
	poetry run black --target-version py311 stacosys/ tests/

test:	
	poetry run coverage run -m --source=stacosys pytest
	poetry run coverage report        

typehint: 
	poetry run mypy --ignore-missing-imports stacosys/

lint:
	poetry run pylint stacosys/

