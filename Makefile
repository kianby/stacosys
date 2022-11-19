all: test typehint lint black 

test:
	pytest

typehint: 
	mypy --ignore-missing-imports stacosys/

lint:
	pylint stacosys/

black:
	black -l 79 stacosys/