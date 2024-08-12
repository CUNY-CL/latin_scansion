# 🏛️ Latin scansion engine 🏛️

[![Supported Python
versions](https://img.shields.io/pypi/pyversions/latin_scansion.svg)](https://pypi.org/project/latin_scansion)
[![CircleCI](https://circleci.com/gh/CUNY-CL/latin_scansion/tree/master.svg?style=svg)](https://circleci.com/gh/CUNY-CL/latin_scansion/tree/master)

This library uses finite-state grammars to automate Latin scansion, with an
initial focus on the dactylic hexameters of Virgil.

## License

The engine is released under an Apache 2.0 license. Please see
[LICENSE.txt](LICENSE.txt) for details.

## Installation

[Conda](http://conda.io) is recommended for a reproducible environment. Assuming
that Conda (either Miniconda or Anaconda) is available, the following command
creates the environment `scansion`.

    conda env create -f environment.yml

This only needs to be done once. The following command then activates the
environment.

    conda activate scansion

This second step needs to be repeated each time you start a new shell.

## Installation

1.  Compile the grammar assets:

        make -j -C grammars

2.  Generate the textproto library:

        make -C latin_scansion

3.  Install the Python library:

        pip install -e .

## Command-line tools

Installation produces two command-line tools:

-   [`latin-scan`](latin_scansion/cli/scan.py) scans a document, generating a
    human-readable
    [textproto](https://medium.com/@nathantnorth/protocol-buffers-text-format-14e0584f70a5)
    representation of document's scansion. Sample usage:

        latin-scan --far grammars/all.far data/Aeneid/Aeneid01.txt data/Aeneid/Aeneid01.textproto

-   [`latin-validate`](latin_scansion/cli/validate.py) validates (and
    optionally, canonicalizes) a textproto document scansion. Sample usage:

        latin-validate data/Aeneid/Aeneid01.textproto

## Testing

Run:

    pytest tests

## Authors

-   [Jillian Chang](jillianchang15@gmail.com)
-   [Kyle Gorman](kgorman@gc.cuny.edu)
