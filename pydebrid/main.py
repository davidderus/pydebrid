# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module of pydebrid. One function to rule them all.
"""

import os
import sys
import argparse
from clint.textui import colored
from core import Alldebrid, PydConfig, URI, Downloader, Subtitle
from core import CaptchaException
import pyperclip
import unicodedata


def main():
    """
    Handles command line input and output
    Do Alldebrid instanciation
    :rtype : None
    """
    args = setup_cli()

    alld = Alldebrid()
    config = PydConfig()

    try:
        username = config.get('user', 'username')
        password = config.get_password(username)
        alld.connect(username, password)
    except CaptchaException, msg:
        print colored.red(msg)
        sys.exit(1)
    except Exception, msg:
        print colored.red(msg)
        config.remove_config()

    if args.i:
        print alld.get_infos(True)
        sys.exit()

    if not args.u:
        print colored.blue('Nothing to do…')
        sys.exit()

    user_infos = alld.get_infos()

    if user_infos['remaining_days'] < 2:
        print colored.red('Your account expires in %s' % user_infos['remaining'])

    url_asked = URI(args.u)

    if url_asked.is_url():
        res = [alld.debrid(url_asked.get_uri())]
    else:
        # We only allow the reading of text/plain files and files without a mime (like a file without extension, as Python can't guess that).
        # It's a basic check, but it's better than nothing.
        if url_asked.get_mimetype() not in (None, 'text/plain'):
            raise Exception("Given local file is not readable by pydebrid. Make sure it's a text/plain file.")
        res = []
        for line in open(url_asked.get_uri()):
            try:
                temp_uri = URI(line)
                tmp = alld.debrid(temp_uri.get_uri())
            except Exception, msg:
                print colored.red('Error with %s: %s' % (line.rstrip(), msg))
            else:
                res.append(tmp)

    if args.d:
        nb_files = len(res)
        for index, link in enumerate(res, start=1):
            filename = URI(link).get_filename()
            if nb_files > 1:
                print colored.blue('--- Downloading %s (%u/%u) ---' % (filename, index, nb_files))
            output = os.path.join(args.o, filename)
            print colored.yellow('Outputing at: %s' % output)
            path = Downloader(alld.get_session()).download(link, output)
            if args.s and path:
                print colored.yellow('Downloading subs…')
                subs = Subtitle(path).set_langs(args.s.split(',')).get()
                print colored.green('…Subs downloaded!') if len(subs) > 0 else colored.red('…No subs found')
    else:
        links = unicodedata.normalize('NFKD', '\r\n'.join(res)).encode('ASCII', 'ignore')
        links_count = len(res)
        if args.stdout:
            print links_to_stdout(links, links_count)
        else:
            print links_to_clipboard(links, links_count)

def links_to_clipboard(links, links_count):
    pyperclip.copy(links)
    if links_count == 0:
        return colored.red('No links debrided')
    elif links_count == 1:
        return colored.green('Success, your link has been copied in your clipboard')
    else:
        return colored.green('Success, your links have been copied in your clipboard')

def links_to_stdout(links, links_count):
    if links_count == 0:
        return colored.red('No links debrided')
    else:
        return links
    sys.exit(0)

def setup_cli():
    """
    Setup parser options for command-line interface
    :return:
    """
    parser = argparse.ArgumentParser(description="""Using your account on Alldebrid.com,
                                    this script will help you debrid one link or a list of link.
                                    By default, it accepts no arguments and asks you your remote file URL.""")

    parser.add_argument('-u', help='Local text/plain file (like links.txt) or remote url (like http://ul.to/abcde)',
                        metavar='File/HTTP URL')
    parser.add_argument('-d', help='Download the linked file(s) once debrided', action='store_true', default=False)
    parser.add_argument('-i', help='Display current user informations', action='store_true', default=False)
    parser.add_argument('-s', help='Get subtitles following a single or comma-separated list of IETF language code',
                        metavar='Subtitles language(s)')
    parser.add_argument('-o', help='Custom file output directory (otherwise current directory)',
                        metavar='Destination directory', default=os.getcwd())
    parser.add_argument('--stdout', help='Output links to STDOUT instead of clipboard', action='store_true', default=False)

    return parser.parse_args()


def launcher():
    try:
        main()
    except Exception, msg:
        print colored.red(msg)
        sys.exit(1)

if __name__ == '__main__':
    launcher()
