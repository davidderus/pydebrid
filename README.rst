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
* Clipboard support by default
* Account information and expiration alert
* Secure config storage
* SSL Support
* Captcha alert
* Intuitive and colorful use
* Cross-platform (Tested on Linux and OS X but should works on Windows too)

Usage
=====

:code:`pydebrid [-h] [-u File/HTTP URL] [-d] [-i] [-s Subtitles languages] [-o Destination directory]`

* ``-h`` : Display help
* ``-u`` : Local txt file (like links.txt) or remote url (like http://ul.to/abcde)
* ``-d`` : Download the linked file(s) once debrided
* ``-i`` : Display current user informations
* ``-s`` : Get subtitles following a single or comma-separated list of IETF language code
* ``-o`` : Custom file output directory (otherwise current directory)

Examples
========

:code:`pydebrid -u http://ul.to/abcde -d -s en,fr`

Download ``http://ul.to/abcde`` in the current directory with english and french subtitles.

:code:`pydebrid -u links.txt`

Unrestrain all links in ``links.txt`` file (one link per line) and put them in the clipboard.

:code:`pydebrid -i`

Return infos from your account like Fidelity points, Remaining time, Registration date and more.