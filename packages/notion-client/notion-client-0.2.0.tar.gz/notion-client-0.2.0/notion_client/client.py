import logging
from dataclasses import dataclass
from typing import Dict, Union

import httpx

from .logging import make_console_logger
from .api_endpoints import DatabasesEndpoint, UsersEndpoint
from .helpers import pick


@dataclass
class ClientOptions:
    auth: str = None
    timeout_ms: int = 60_000
    base_url: str = "https://api.notion.com"
    log_level: int = logging.WARNING
    logger: logging.Logger = None
    notion_version: str = "2021-05-13"


class Client:
    def __init__(
        self,
        options: Union[Dict, ClientOptions] = None,
        client: httpx.Client = None,
        **kwargs,
    ):
        if options is None:
            options = ClientOptions(**kwargs)
        elif isinstance(options, dict):
            options = ClientOptions(**options)

        self.log_level = options.log_level
        self.logger = options.logger or make_console_logger()

        if client is None:
            client = httpx.Client()
        self.client = client
        self.client.base_url = options.base_url + "/v1/"
        self.client.timeout = options.timeout_ms / 1_000
        self.client.headers = {
            "Notion-Version": options.notion_version,
            "User-Agent": "ramnes/notion-sdk-py@0.2.0",
        }
        if options.auth:
            self.client.headers["Authorization"] = f"Bearer {options.auth}"

        self.databases = DatabasesEndpoint(self)
        self.users = UsersEndpoint(self)

    def request(self, path, method, query=None, body=None, auth=None):
        self.logger.info("request start", method, path)

        request = self.client.build_request(method, path)

        return self.client.send(request)

    def search(self, **kwargs):
        return self.request(
            path="search",
            method="POST",
            body=pick(kwargs, "query", "sort", "filter", "start_cursor", "page_size")
        )
