========
pydebrid
========

A simple & cross-platform command-line interface for unrestraining links thanks to Alldebrid.

Features
========

* Links unleashing
* Bulk unleashing (from txt file)
* Embed downloader
* Multi-languages subtitles getter
* Clipboard or STDOUT output
* Account information and expiration alert
* Secure config storage
* SSL Support
* Captcha alert
* Intuitive and colorful use
* Cross-platform (Tested on Linux and OS X but should works on Windows too)

Installation
============
pydebrid is available on PyPI. In order to install it, just use the following command :

``pip install pydebrid``


Usage
=====

:code:`pydebrid [-h] [-u File/HTTP URL] [-d] [-i] [-s Subtitles languages] [-o Destination directory] [--stdout]`

* ``-h`` : Display help
* ``-u`` : Local text/plain file (like links.txt) or remote url (like http://ul.to/abcde)
* ``-d`` : Download the linked file(s) once debrided
* ``-i`` : Display current user informations
* ``-s`` : Get subtitles following a single or comma-separated list of IETF language code
* ``-o`` : Custom file output directory (otherwise current directory)
* ``--stdout`` : Output links to STDOUT instead of clipboard

Examples
========

:code:`pydebrid -u http://ul.to/abcde -d -s en,fr`

Download ``http://ul.to/abcde`` in the current directory with english and french subtitles.

:code:`pydebrid -u links.txt`

Unrestrain all links in ``links.txt`` file (one link per line) and put them in the clipboard.

:code:`pydebrid -i`

Return infos from your account like Fidelity points, Remaining time, Registration date and more.

Changelog
=========

From 1.0.8 to 1.0.9:

- Bugfix (see https://github.com/davidderus/pydebrid/issues/6)

From 1.0.6 to 1.0.7:

- Updating root URL for Alldebrid website

From 1.0.4 to 1.0.6:

- New requests version
- New subliminal version
- Output to STDOUT (Issue #1)

Future
======

- Resuming download on failure (Issue #2)
