all: black test typehint lint 

black:
	isort --multi-line 3 --profile black stacosys/
	black stacosys/

test:
	pytest

typehint: 
	mypy --ignore-missing-imports stacosys/

lint:
	pylint stacosys/

