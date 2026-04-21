from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_bitso.feeds.live_bitso import BitsoRequestData


def test_bitso_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = BitsoRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="BITSO___SPOT",
    )

    monkeypatch.setattr(
        request_data,
        "http_request",
        lambda method, url, headers, body, timeout: {"success": True, "payload": []},
    )

    result = request_data.request("GET /available_books")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"success": True, "payload": []}
