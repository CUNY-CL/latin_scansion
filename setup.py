import os
import setuptools


_VERSION = "0.1.2"

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(_THIS_DIR, "README.md")) as f:
    _LONG_DESCRIPTION = f.read().strip()


def main():
    setuptools.setup(
        name="latin_scansion",
        version=_VERSION,
        author="Jillian Chang, Kyle Gorman",
        author_email="kylebgorman@gmail.com",
        description="Automated Latin scansion",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/CUNY-CL/latin_scansion",
        keywords=[
            "computational linguistics",
            "natural language processing",
            "phonology",
            "phonetics",
            "speech",
            "language",
            "Latin",
        ],
        license="Apache 2.0",
        packages=setuptools.find_packages(),
        python_requires=">=3.7",
        zip_safe=False,
        setup_requires=["setuptools>=39"],
        install_requires=["protobuf>=3.20.2"],
        entry_points={
            "console_scripts": [
                "latin-scan = latin_scansion.scan:main",
                "latin-validate = latin_scansion.validate:main",
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Text Processing :: Linguistic",
        ],
        data_files=[(".", ["LICENSE.txt"])],
    )


if __name__ == "__main__":
    main()
