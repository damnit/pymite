.PHONY: status

htmlcov:
	py.test -vvs --cov=pymite --cov-report=html
	cd htmlcov && python -m http.server && cd ..

develop:
	pip install -r dev-requirements.txt

test:
	@py.test -vvs

release:
	python setup.py sdist bdist_wheel upload
