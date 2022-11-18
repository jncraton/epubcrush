all:

format:
	black epubcrush/epubcrush.py

upload:
 python3 setup.py sdist bdist_wheel
 python3 -m twine upload dist/*

clean:
 rm -rf tmp
 rm -rf epubcrush.egg-info
 rm -rf epubcrush/__pycache__
 rm -rf dist
 rm -rf build
