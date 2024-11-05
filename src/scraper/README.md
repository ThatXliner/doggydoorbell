# Scraper

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![codecov](https://codecov.io/gh/ThatXliner/scraper/branch/main/graph/badge.svg)](https://codecov.io/gh/ThatXliner/scraper)

[![CI](https://github.com/ThatXliner/scraper/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ThatXliner/scraper/actions/workflows/ci.yml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scraper)](https://pypi.org/project/scraper)
[![PyPI](https://img.shields.io/pypi/v/scraper)](https://pypi.org/project/scraper)
[![PyPI - License](https://img.shields.io/pypi/l/scraper)](#license)

> Download the dataset

## Installation

You can get this project via `pip`

```bash
$ pip install scraper
```


But we **highly recommend** you install this project using [pipx](https://pypa.github.io/pipx/)

```bash
$ pipx install scraper
```

## How to use

For any dataset on AudioSet, you can download all of the YouTube videos being previewed on the page by this process.

First, navigate to the page in your browser, and scroll all the way do load all the files. After that, run this JavaScript code in the console to get all the links.

```js
[...document.querySelectorAll("[src^='https://img.youtube.com/vi']")].map(x=>x.src)
```

Then, save the output to a file (stored somewhere; will be `~/links.json` for this example), and run the following command to download all the videos.

```bash
poetry run python -m scraper ~/links.json
```
Finally, you can convert all the videos to mp3 files using the following command.

```bash
for i in *; do ffmpeg -i "./$i" "./${i%.*}.mp3"; done
```


## License

This project is licensed under the [GNU GPL v3+](https://github.com/ThatXliner/scraper/blob/main/LICENSE.txt).

In short, this means you can do anything with it (distribute, modify, sell), but if you were to publish your changes, you must make the source code and build instructions readily available.

If you are a company using this project and want an exception, email me at [thatxliner@gmail.com](mailto:thatxliner@gmail.com), and we can discuss it.
