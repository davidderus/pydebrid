# -*- coding: utf-8 -*-

"""
A global yet simple Alldebrid wrapper
"""

import requests
from bs4 import BeautifulSoup
import re


class Alldebrid:
    """
    Alldebrid class, allowing interaction with their API
    """

    ALLDEBRID_ROOT = 'https://alldebrid.com'

    # Website links
    infos = {
        'login': ALLDEBRID_ROOT + '/register/',
        'infos': ALLDEBRID_ROOT + '/account/',
        'rapidDebrid': ALLDEBRID_ROOT + '/service.php',
        'ua': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    def __init__(self):
        self.logged = False
        self.session = None
        self.user = None
        self.all_infos = None

    def connect(self, username, password):
        """
        Log the user to Alldebrid
        :param username: Given username
        :param password: Given password
        :return: A boolean if it's all right, exception otherwise
        """

        # Current params used for connection
        connect_params = {
            'action': 'login',
            'returnpage': '/account/',
            'login_login': username,
            'login_password': password
        }

        # We start a session to keep login trace
        self.session = requests.Session()

        connection = self.session.get(self.infos['login'], params=connect_params,
                                      headers={'User-Agent': self.infos['ua']})

        soup = BeautifulSoup(connection.text, 'lxml')

        if connection.url != self.infos['infos']:
            captcha = soup.find(class_='login').find(attrs={'name': 'recaptcha_response_field'})

            if captcha > 0:
                raise CaptchaException(
                    """Due to numerous attemps to login, there is a captcha to solve.\n
                    Please use your web browser to login first and then try to login with pydebrid.""")
            else:
                raise Exception(
                    'Error while trying to log in with username %s.\nPlease check your credentials or your connectivity.' % repr(
                        username))

        self.logged = True

        self.user = self.__parse_infos(soup)

        return True

    def debrid(self, url):
        """
        Debrid function, returning a debrided link or a None value
        :param url: The URL to debug
        :return: Debrided link or none value
        """
        if not self.logged:
            raise Exception('You must be connected in order to debrid')

        try:
            debrid_page = self.session.get(self.infos['rapidDebrid'], params={'link': url, 'json': 'true'},
                                           headers={'User-Agent': self.infos['ua']})
        except requests.exceptions.RequestException, msg:
            raise Exception(msg)
        else:
            json = debrid_page.json()

            if json['error']:
                raise Exception(json['error'])
            else:
                debrided = json['link']

            if debrided is None or debrided == url or debrided.find('http://www.alldebrid.com/service.php') != -1:
                raise Exception('Can\'t debrid this link')
            else:
                return debrided

    def get_infos(self, show_all=False):
        """
        Get infos from the user (in cache or by making a request)
        :param show_all: Directly print the user infos from the website or not
        :return: A dict containing all user infos
        """
        if not self.logged:
            raise Exception('You must be connected in order to get your account infos')

        if show_all and self.all_infos:
            return self.all_infos
        elif not show_all and self.user:
            return self.user

        infos_page = self.session.get(self.infos['infos'], headers={'User-Agent': self.infos['ua']})

        if infos_page.status_code is not 200 or not infos_page.url == self.infos['infos']:
            raise Exception('Can\'t get your infos')

        soup = BeautifulSoup(infos_page.text, 'lxml')
        user_infos = self.__parse_infos(soup, show_all)

        self.user = user_infos
        return user_infos

    def __parse_infos(self, soup, show_all=False):
        """
        Parse infos from the account html page
        :param soup: The account page HTML
        :param show_all: Directly print the user infos from the website or not
        :return: A dict containing all user infos
        """

        part_one = soup.find(class_='account_infopartone')
        # Removing email field and associated JS as it's secured (and a useless info)
        part_one.findAll('li')[2].extract()

        class_infos_one_text = part_one.text.replace('\n\n', '\n').replace('\t', '').strip()
        class_infos_two_text = soup.find(class_='account_infoparttwo').text.replace('\t', '')
        class_infos_texts = class_infos_one_text + class_infos_two_text

        try:
            remaining_days = soup.find(class_='remaining_days').find('span').text
        except Exception:
            remaining_days = 0

        try:
            exact_remaining = soup.find(class_='remaining_time_text').find('strong').text.strip()
        except Exception:
            exact_remaining = None

        if show_all:
            clean_infos = class_infos_texts.replace(' (Extend)', '')
            clean_infos = clean_infos.replace(' (Use)', '')
            clean_infos = re.sub(r'\s\([0-9]*\spts\sneeded\)', '', clean_infos)
            clean_infos = re.sub(r'You currently have : [0-9]*\s\w*\n', '', clean_infos)
            clean_infos += 'Remaining time : %s' % exact_remaining
            self.all_infos = clean_infos
            return clean_infos

        class_infos_dict = dict(element.split(' : ') for element in filter(None, class_infos_texts.split('\n')) if ' : ' in element)

        user_infos = {
            'remaining': exact_remaining,
            'remaining_days': int(remaining_days),
            'registration': class_infos_dict['Registered since'],
            'points': class_infos_dict['Fidelity points'].split(' ')[0],
            'subscription': class_infos_dict['Subscription']
        }

        return user_infos

    def get_session(self):
        """
        Get the current Alldebrid session
        :return: The current Alldebrid session
        """
        return self.session


class CaptchaException(Exception):
    """
    Custom exception made thrown when a captcha is present on login page
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
