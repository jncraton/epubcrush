all:

epubcheck:
	wget -q -O epubcheck.zip https://github.com/w3c/epubcheck/releases/download/v4.2.6/epubcheck-4.2.6.zip && unzip -q epubcheck.zip && rm -f epubcheck.zip

test: lint epubcheck
	python3 -m doctest epubcrush/epubcrush.py
	python3 compare.py

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
	rm -rf epubcheck
