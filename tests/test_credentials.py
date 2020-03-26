from unittest import TestCase
import json
import os

from api.credentials import init_credentials, parse_credentials, BadLogin, BadCookies, BadCredentialsFile
from api.arguments import get_parser


class Test(TestCase):
    # Login by cookies simulating command line arguments
    def test_credentials_cookie(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_cookies.json"])
        init_credentials(args.credentials_file_path, write_new_cookies=False)

    # Login by username simulating command line arguments
    def test_credentials_login(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_login.json"])
        init_credentials(args.credentials_file_path, write_new_cookies=False)

    # Bad structures for credentials file
    def test_credentials_bad_data(self):
        url = ''
        cookies = ''
        login_info = {'username': '', 'password': ''}

        try:
            parse_credentials({'cookies': cookies, 'login_info': login_info})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.no_url

        try:
            parse_credentials({'url': url})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.no_cookies_or_login

        try:
            parse_credentials({'url': url, 'login_info': {}})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.incomplete_login

        try:
            parse_credentials({'url': url, 'cookies': cookies, 'login_info': {}})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.incomplete_login

        try:
            parse_credentials({'url': url, 'cookies': cookies, 'login_info': {'username': ''}})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.incomplete_login

        try:
            parse_credentials({'url': url, 'cookies': cookies, 'login_info': {'password': ''}})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.incomplete_login

        try:
            parse_credentials({'url': url, 'cookies': cookies, 'fallback_on_login': True})
            raise Exception
        except BadCredentialsFile as e:
            assert e.e_type == BadCredentialsFile.fallback_with_no_login

    # Detect bad cookies + fallback for username
    def test_credentials_bad_login(self):
        try:
            init_credentials('./tests/configs/credentials_static_login_bad.json')
            raise Exception
        except BadLogin:
            pass

    # Detect bad cookies
    def test_credentials_bad_cookies(self):
        try:
            init_credentials('./tests/configs/credentials_static_cookies_bad.json')
            raise Exception
        except BadCookies:
            pass

    # Login by username, dump cookies, login by cookies
    def test_dump_cookies(self):
        aux_file_path = "./tests/configs/tmp-credentials.json"
        with open("./tests/configs/credentials_static_login.json") as json_file:
            data = json.load(json_file)

        data['credentials_file_path'] = aux_file_path
        parse_credentials(data)

        with open(aux_file_path) as json_file:
            data = json.load(json_file)

        data.pop('fallback_on_login')
        data.pop('login_info')
        parse_credentials(data)

        os.remove(aux_file_path)
