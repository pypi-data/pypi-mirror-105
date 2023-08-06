import os
from functools import lru_cache
from typing import Any, Optional

import requests
from requests import Response

from tikkie._version import VERSION
from tikkie.errors import BaseError

API_KEY_ENV = "TIKKIE_API_KEY"
APP_TOKEN_ENV = "TIKKIE_APP_TOKEN"
API_URL_ENV = "TIKKIE_API_URL"


class ApiSession(requests.Session):
    def __init__(self, *, app_token: str, api_key: str, api_url: str):
        super().__init__()
        self.api_url = api_url
        self.app_token = app_token
        self.api_key = api_key
        self.headers["User-Agent"] = f"Python Tikkie API/{VERSION}"

    def prepare_request(self, request: Any) -> Any:
        request.url = "/".join(s.strip("/") for s in [self.api_url, "v2/tikkie", request.url])
        return super().prepare_request(request)

    def request(
        self,
        *args: Any,
        params: Any = None,
        app_token: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> Response:
        dict_params = params or {}
        headers = kwargs.pop("headers", {})

        headers["X-App-Token"] = app_token or self.app_token
        headers["API-Key"] = api_key or self.api_key

        # Manually convert the json objects as we want to use a custom encoder
        # if "json" in kwargs:
        #     payload = kwargs.pop("json")
        #     kwargs["data"] = json.dumps(payload, cls=JSONEncoder)
        #     headers["Content-Type"] = "application/json"

        r = super().request(*args, params=dict_params, headers=headers, **kwargs)  # type: ignore
        if not r.ok:
            raise BaseError.from_response(r)
        return r


# The global session object
_session: Optional[ApiSession] = None


def _read_from_os(var: Optional[str], env: str) -> Optional[str]:
    if var is None:
        var = os.environ.get(env)
    return var


@lru_cache()
def get_session() -> ApiSession:
    global _session
    if _session is None:
        configure()
    return _session  # type: ignore


def configure(
    *, app_token: Optional[str] = None, api_key: Optional[str] = None, api_url: Optional[str] = None
) -> None:
    global _session

    app_token = _read_from_os(app_token, APP_TOKEN_ENV)
    api_key = _read_from_os(api_key, API_KEY_ENV)
    api_url = _read_from_os(api_url, API_URL_ENV)

    if not api_url:
        raise Exception("The API Url is not set")

    get_session.cache_clear()

    _session = ApiSession(app_token=app_token, api_url=api_url, api_key=api_key)
