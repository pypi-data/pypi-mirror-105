import os
import requests
from functools import lru_cache
from requests import Response
from typing import Any, Optional

from tikkie.errors import BaseError

API_KEY_ENV = "TIKKIE_API_KEY"
APP_TOKEN_ENV = "TIKKIE_APP_TOKEN"
API_URL_ENV = "TIKKIE_API_URL"


class ApiSession(requests.Session):
    def __init__(self, *, app_token: str, api_key: str, api_url: str):
        super().__init__()
        self.api_url = api_url
        # self.app_token = app_token
        self.headers["X-App-Token"] = app_token
        self.headers["API-Key"] = api_key
        # self.app_token = app_token
        # self.timeout = API_TIMEOUT

    def prepare_request(self, request: Any) -> Any:
        request.url = "/".join(s.strip("/") for s in [self.api_url, "v2/tikkie", request.url])
        return super().prepare_request(request)

    def request(self, *args: Any, params: Any = None, **kwargs: Any) -> Response:
        dict_params = params or {}
        headers = kwargs.pop("headers", {})
        # headers.setdefault("X-App-Token", self.app_token)

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


def _read_from_os(var: Optional[str], env: str) -> str:
    if var is None:
        var = os.environ.get(env)
        if var is None:
            raise Exception(f"Api not configured, please set the {env} environment variable")
    return var


@lru_cache()
def session() -> ApiSession:
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

    session.cache_clear()

    _session = ApiSession(app_token=app_token, api_url=api_url, api_key=api_key)
