all:

test:
	python3 -m doctest epubcrush/epubcrush.py

format:
	black epubcrush/epubcrush.py compare.py
	black setup.py

lint:
	flake8 --max-line-length 88 epubcrush/epubcrush.py compare.py
	mypy epubcrush/epubcrush.py

upload:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

clean:
	rm -rf tmp
	rm -rf epubcrush.egg-info
	rm -rf epubcrush/__pycache__
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf build
