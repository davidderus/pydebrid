# -*- coding: utf-8 -*-

from urlparse import urlparse

import os
import re
import mimetypes
import unicodedata

class URI:
    """
    Global URI toolkit
    """
    urlParse = None

    def __init__(self, uri):
        """
        Instantiate a new URI
        :param uri: The URI to work with
        """
        temp_uri = unicodedata.normalize('NFKD', unicode(uri)).encode('ASCII', 'ignore')
        self.uri = str(temp_uri).strip()
        if os.path.isfile(uri):
            self.file = True
            self.url = False
        elif self.__is_valid_url():
            self.file = False
            self.url = True
        else:
            raise Exception('Invalid type for URI. Given uri is not a file nor a valid URL.')

    def is_file(self):
        """
        Is URI a file?
        :return: A boolean
        """
        return self.file

    def is_url(self):
        """
        Is URI an URL?
        :return: A boolean
        """
        return self.url

    def __is_valid_url(self):
        """
        Is this URL a valid one?
        :return: A boolean
        """
        self.urlParse = urlparse(self.uri)

        if self.urlParse.scheme in ('http', 'https') and self.urlParse.netloc and self.urlParse.path:
            return True
        else:
            return False

    def get_uri(self):
        """
        Return the full URI
        :return: The full URI
        """
        return self.uri

    def get_filename(self):
        """
        Get the filename from the URL
        :return: The filename
        """
        if not self.urlParse:
            self.__is_valid_url()

        path = self.urlParse.path
        # (((?!\/).)*.[\w\d]{2,4})$
        match = re.search(r"(((?!\/).)*.[\w\d]{2,4})$", path)
        if match:
            filename = match.group(1)
        else:
            raise Exception("Can't guess filename")

        return filename

    def get_mimetype(self):
        """
        Get the mimetype of a file
        :return: A mimetype or None
        """
        mimetype, encoding = mimetypes.guess_type(self.uri)
        return mimetype

    def __str__(self):
        return self.uri