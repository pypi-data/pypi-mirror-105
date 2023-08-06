# **apread** (Catman AP Reader)
> Read binary files produced from catmanAP projects directly into python.

CatmanAP procudes .bin files after each measurement. While it is possible to export as a different format (i.e. txt or asc) it's not efficient because one has to change the export format after every measurement. Here comes the treat: Just export as binary and use this package to work with binary files directly.

## Installation

Anywhere with python:

```sh
pip install apread
```


## Usage example

Lets say you produced a file called `measurements.bin` and you put it in the directory of your python script.

```python
from apread import APReader

reader = APReader('measurements.bin')
``` 
It's that simple.



## Release History

* Version 1.0.0
    * Convert catman files to channels

## Publish

### Modify `setup.py`
Apply a new version and update `README.md`
### Build the project
```python
python setup.py sdist bdist_wheel
```
### Upload the project
```python
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

## Meta

Leon Bohmann – info@leonbohmann.de

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/leonbohmann/apreader](https://github.com/leonbohmann/apreader)