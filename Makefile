shell:
	pipenv shell --python 3.6 || true

test: shell
	mypy --ignore-missing-imports kubectl
	pytest -vv