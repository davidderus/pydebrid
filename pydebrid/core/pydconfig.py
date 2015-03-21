# -*- coding: utf-8 -*-

import ConfigParser
import getpass
import sys

from clint.textui import prompt, colored
import os
import keyring


class PydConfig(ConfigParser.ConfigParser):
    """
    Alldebrid config getter/setter
    ==============================

    Depends on ConfigParser and keyring module
    """

    keyring = 'pydebrid'
    config_path = os.path.join(os.path.expanduser('~'), '.pydebrid')
    config_file_path = os.path.join(config_path, 'pydconfig.cfg')

    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)
        self.read(self.config_file_path)

        if not self.has_section('user'):
            self.create_config()

    def create_config(self):
        """
        Interactive config creation
        """
        print colored.blue(
            "Welcome! It's the first time you launch pydebrid so you need to give us a few credentials.")

        input_username = prompt.query("What's your Alldebrid username?")
        input_password = getpass.getpass('And your password? ')

        self.add_section('user')
        self.set('user', 'username', input_username)
        self.__set_password(input_username, input_password)

        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

        with open(self.config_file_path, 'wb') as configfile:
            self.write(configfile)

        print colored.green('Okay, config set!')

    def __set_password(self, username, password):
        """
        Set a password associated to a username in the keyring
        :param username: Username for the password
        :type username: str
        :param password: User password
        :type password: str
        """
        keyring.set_password(self.keyring, username, password)

    def get_password(self, username):
        """
        Return the password associated to this username in keyring
        :param username: Username for the password
        :type username: str
        """
        return keyring.get_password(self.keyring, username)

    def __delete_password(self, username):
        """
        Delete the password associated to this username in keyring
        :param username: Username for the password
        :type username: str
        """
        keyring.delete_password(self.keyring, username)

    def remove_config(self):
        """
        Interactive config removal
        """
        reset = prompt.yn('Would you like to reset config?')
        if reset:
            username = self.get('user', 'username')
            os.remove(self.config_file_path)
            self.__delete_password(username)
            print colored.green('Config removed')
        sys.exit()
