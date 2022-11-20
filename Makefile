all: test typehint lint black 

test:
	pytest

typehint: 
	mypy --ignore-missing-imports stacosys/

lint:
	pylint stacosys/

black:
	isort --multi-line 3 --profile black stacosys/
	black stacosys/