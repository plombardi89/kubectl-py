shell:
	pipenv shell --python 3.6 || true
	pipenv sync

test: shell
	mypy --ignore-missing-imports kubectl
	pytest -vv