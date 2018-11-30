import requests
from secrets import token_urlsafe


# def xstr(s):
#     return s if s else ''


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)


class AccountsHelper:
    def __init__(self, *, server_url=None, auth=None):
        self.url = server_url
        self.auth = auth

    def create_user(self, username):
        r = requests.delete(f'{self.url}/accounts/{username}',
                            auth=self.auth)
        password = token_urlsafe(5)
        r = requests.post(f'{self.url}/accounts',
                          json={'data': {'id': username, 'password': password}},
                          auth=self.auth)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(r.text)
            raise e

        return password
