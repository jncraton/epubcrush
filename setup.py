import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epubcrush",
    version="1.0.0",
    author="Jon Craton",
    author_email="jon@joncraton.com",
    description="Compress EPUB files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jncraton/epubcrush",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "epubcrush=epubcrush:main",
        ],
    },
    install_requires=[],
)
