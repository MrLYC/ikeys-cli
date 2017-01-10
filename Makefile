.PHONY: test
test:
	env PYTHONPATH=. py.test -v tests

.PHONY: upload
upload:
	python setup.py sdist upload
	git tag `python setup.py --version`
