import os
import platform
import json
import click

import requests

from .exceptions import MdException
from .api import (
    AccountAPI, AuthAPI, AuthorAPI, ChapterAPI, GroupAPI, ListAPI, MangaAPI,
    MiscAPI, UserAPI
)


class APIHandler:
    UA = f"PyMyAPI on Python {platform.python_version()}"
    BASE = "https://api.mangadex.org"

    AUTH_FILE = ".mdauth"

    def __init__(self, md):
        self.md = md
        self.user = None
        self._auth = None
        self._load_auth()

    def _save_auth(self):
        with open(self.AUTH_FILE, "w") as auth_file:
            json.dump({
                "user": self.user,
                "_auth": self._auth
            }, auth_file)

    def _load_auth(self):
        if not os.path.exists(self.AUTH_FILE):
            return

        with open(self.AUTH_FILE) as auth_file:
            try:
                auth = json.load(auth_file)
            except json.JSONDecodeError:
                return

        try:
            user = auth["user"]
            _auth = auth["_auth"]
        except KeyError:
            return

        self.user = user
        self._auth = _auth

    def _get_headers(self):
        headers = {}
        if self._auth is not None:
            headers["Authorization"] = "Bearer " + self._auth.get("session")
        headers["User-Agent"] = self.UA
        return headers

    def _make_request(self, action, body=None, params=None, urlparams=None):
        url = self.BASE + action[1].format(**(urlparams or {}))
        req = requests.request(
            action[0], url,
            json=body,
            params={k: v for k, v in (params or {}).items() if v is not None},
            headers=self._get_headers()
        )
        click.echo(click.style(f" -> {action[0]} {req.url}", fg="yellow"))

        if req.status_code == 204:
            resp = {}
        else:
            resp = req.json()
        if req.status_code < 200 or req.status_code > 299:
            raise MdException(resp.get("errors", []))

        if not isinstance(resp, dict):
            return resp
        if "data" in resp:
            data = resp["data"]
            if "relationships" in resp:
                data["relationships"] = resp["relationships"]
            resp = data
        return resp

    def _authenticate(self, username, token):
        self._auth = token
        if token is None or username is not None:
            self.user = {"username": username}
        self._save_auth()

    def _get_refresh_token(self):
        if self._auth:
            return self._auth["refresh"]
        return None


class MdAPI:
    def __init__(self):
        self.api = APIHandler(self)

        self.account = AccountAPI(self.api)
        self.auth = AuthAPI(self.api)
        self.author = AuthorAPI(self.api)
        self.chapter = ChapterAPI(self.api)
        self.group = GroupAPI(self.api)
        self.list = ListAPI(self.api)
        self.manga = MangaAPI(self.api)
        self.misc = MiscAPI(self.api)
        self.user = UserAPI(self.api)
