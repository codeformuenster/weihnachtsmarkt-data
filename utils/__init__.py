import requests


def xstr(s):
    return s if s else ''


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


class BoothPoster:
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def post(self, booth):
        del_none(booth)
        r = requests.post(self.url,
                          json={'data': booth}, auth=self.auth)
        r.raise_for_status()
