# Static-Site-Generator

This program builds a static site in two steps:

1. It takes a directory of Markdown files and for each file the program copies, converts and modifies it into a new HTML file with the same content. This new file is saved into a new _destination_ directory.
2. It copies a directory of any kind of files and converts them in the _destination_ directory with the HTML files

The _source_ directories may contain nested directories of arbitrary depth. The program will search in directories at any level and copy the same structure inside the _destination_ directory.

As we said, the program has two sources and one destination. These three directories have hard-coded default names.

- Markdown source name is **content**. If the directory doesn't exist an error occurs.
- the other source name is **static**. If the directory doesn't exist an error occurs.
- HTML destination name is **docs**. Before either operation, the **docs** directory is completely removed and replaced with an empty one.

## Usage

We can run the program with the command

```bash
python3 src/main.py
```

I've also written a simple script to do that and automatically serve the static site with the python http module

```bash
./main.sh
```

As shown, the script can be executed without arguments., but it can accept one. We can provide a string. The string will be used to _build_ the HTML files slightly differently. What happens is that every link, by default, is copied and pasted as it is from the Markdown files. If we pass a string as input, it will be put as root of every link.

By default, every Markdown link that starts with "/" is treated as an absolute path from the root of the website. This works when the website is served from the domain root. However, GitHub Pages serves project websites under "/REPOSITORY_NAME/" rather than "/". For this reason the program accepts an optional argument specifying the site's base path. Every absolute link is automatically prefixed with that path during generation.

In conclusion, to serve a static site generated with this program using the GitHub's hosting service [Pages](https://docs.github.com/en/pages) just use the command

```bash
python3 src/main.py "/REPO-NAME/"
```

## Warnings

This program assumes that the Markdown files are correctly written. If a syntax error occurs the behaviour of this program is undefined.

## Features

- Recursive directory traversal
- Markdown to HTML conversion
- Static asset copying
- Template-based page generation
- Automatic generation of index pages
- Recursive handling of nested directories
- Configurable base path for GitHub Pages deployment