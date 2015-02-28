# -*- coding: utf-8 -*-

from sys import platform as __platform__

import os
import time
import requests
from clint.textui import progress


class Downloader:
    """
    Allow file download from a distant URL thanks to a requests stream
    """

    def __init__(self, session=None):
        """
        Downloader init, where a previous session can be set
        :param session: A previous session if needed
        """
        if session:
            self.req = session
        else:
            self.req = requests

    def download(self, url, path):
        """
        Download a remote file
        :param url: Remote URL
        :param path: Destination directory
        :return: Destination full file path

        .. todo:: Fix OSX bug where we have to replace https by http
        """
        if __platform__ == 'darwin':
            url = url.replace('https', 'http')

        path = self.__control_path(path)

        req = self.req.get(url, stream=True, timeout=30)

        if req.status_code is not 200:
            raise Exception('Can\'t get file')

        with open(path, 'wb') as dest_file:
            total_length = int(req.headers.get('content-length'))
            if total_length > 0:
                try:
                    for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1,
                                              label='Downloading: '):
                        if chunk:
                            dest_file.write(chunk)
                            dest_file.flush()
                    return path
                except KeyboardInterrupt:
                    # Removing file to prevent broken files on user computer
                    os.remove(path)
                    raise Exception('Download interrupted by user')
            else:
                raise Exception('Empty file size')

    @staticmethod
    def __control_path(path):
        """
        Check if file already exist and other things
        :return: The same path or a new one if there is already a file
        """

        # Make intermediate directory if non-existent
        full_path = os.path.dirname(path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        # Check if file already exists
        if os.path.isfile(path):
            file_name, file_extension = os.path.splitext(path)
            new_path = file_name + time.strftime('_%s_') + file_extension
        else:
            new_path = path

        return new_path
