# SSG

A simple Python-based static site generator.

This repository converts Markdown content under `content/` into static HTML pages in `public/`, using `template.html` and copies static assets from `static/`.

## Features

- Recursively converts `.md` files in `content/` into `.html`
- Extracts page titles from Markdown headings
- Applies a reusable HTML template
- Copies static files into the generated output
- Includes a lightweight local development server script

## Project Structure

- `src/`
  - `main.py` - entrypoint for site generation
  - `markdown_helper.py` - Markdown block parsing and title extraction
  - `htmlnode.py`, `textnode.py`, `block.py`, `splithelper.py` - internal HTML/Markdown node handling
  - `test_*.py` - unit tests
- `content/` - source Markdown pages
- `template.html` - HTML layout template
- `static/` - static assets copied to `public/`
- `public/` - generated website output
- `main.sh` - generate site and start local HTTP server
- `test.sh` - run tests

## Requirements

- Python 3

## Usage

```bash
python3 main.py
```

Or run the bash script to generate and serve using python

```bash
./main.sh
```

To run unit test

```bash
./test.sh
```
