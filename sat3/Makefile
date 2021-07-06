install:
	pip3 install --upgrade pip
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	pip3 install dist/*.whl
	rm -rf dist build *.egg-info

uninstall:
	pip3 uninstall -y $(shell basename $(CURDIR))
