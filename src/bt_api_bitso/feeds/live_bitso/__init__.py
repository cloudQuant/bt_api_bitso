from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.logging_factory import get_logger
from bt_api_base.rate_limiter import RateLimiter, RateLimitRule

from bt_api_bitso.exchange_data import BitsoExchangeData
from bt_api_bitso.tickers import BitsoRequestTickerData


class BitsoRequestData(Feed, RequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_DEALS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_SERVER_TIME,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.public_key = kwargs.get("public_key") or kwargs.get("api_key")
        self.private_key = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.asset_type = kwargs.get("asset_type", "spot")
        self.exchange_name = "BITSO"
        self.logger_name = kwargs.get("logger_name", "bitso_feed.log")
        self._params = BitsoExchangeData()
        self.request_logger = get_logger("request")
        self.async_logger = get_logger("async_request")
        self._rate_limiter = kwargs.get("rate_limiter", self._create_default_rate_limiter())

    @staticmethod
    def _create_default_rate_limiter():
        return RateLimiter(
            rules=[
                RateLimitRule(
                    name="bitso_public",
                    type="request_count",
                    interval=1,
                    limit=60,
                    scope="ip",
                ),
            ],
        )

    def _generate_signature(self, payload: str) -> str:
        if self.private_key is None:
            return ""
        return hmac.new(self.private_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def _build_auth_headers(self, method: str, path: str, payload: str = "") -> dict:
        headers = {"Content-Type": "application/json"}
        if self.public_key is not None:
            headers["Authorization"] = f"Bearer {self.public_key}"
            if payload:
                headers["Signature"] = self._generate_signature(payload)
        return headers

    @staticmethod
    def _extract_data_normalize_function(input_data, extra_data):
        if input_data is None:
            return [], False
        if isinstance(input_data, dict):
            if input_data.get("success"):
                payload = input_data.get("payload", [])
                if isinstance(payload, list):
                    return payload, True
                return [payload], True
            return [input_data], True
        if isinstance(input_data, list):
            return input_data, True
        return [], False

    def request(self, path, params=None, body=None, extra_data=None, timeout=10):
        if params is None:
            params = {}
        is_post = body is not None
        payload = json.dumps(body) if body else ""
        headers = self._build_auth_headers("POST" if is_post else "GET", path, payload)
        url = f"{self._params.rest_url}{path}"
        return self._http_client.request(
            "POST" if is_post else "GET",
            url,
            params=params,
            json=body,
            headers=headers,
            timeout=timeout,
            rate_limiter=self._rate_limiter,
        )

    def async_request(self, path, params=None, body=None, extra_data=None, timeout=10):
        if params is None:
            params = {}
        is_post = body is not None
        payload = json.dumps(body) if body else ""
        headers = self._build_auth_headers("POST" if is_post else "GET", path, payload)
        url = f"{self._params.rest_url}{path}"
        return self._http_client.async_request(
            "POST" if is_post else "GET",
            url,
            params=params,
            json=body,
            headers=headers,
            timeout=timeout,
            rate_limiter=self._rate_limiter,
        )

    def async_callback(self, response, extra_data=None):
        return response
