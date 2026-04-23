from __future__ import annotations

from typing import Any

from bt_api_base.functions.utils import update_extra_data
from bt_api_base.logging_factory import get_logger

from bt_api_bitso.feeds.live_bitso import BitsoRequestData
from bt_api_bitso.tickers import BitsoRequestTickerData


class BitsoRequestDataSpot(BitsoRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        kwargs["asset_type"] = "spot"
        kwargs.setdefault("logger_name", "bitso_spot_feed.log")
        super().__init__(data_queue, **kwargs)
        self.request_logger = get_logger("request")
        self.async_logger = get_logger("async_request")

    def _get_ticker(self, symbol, extra_data=None, **kwargs) -> Any:
        request_symbol = self._params.get_symbol(symbol)
        path = f"/ticker?book={request_symbol}"
        extra_data = update_extra_data(
            extra_data,
            request_type="get_ticker",
            symbol_name=symbol,
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=BitsoRequestDataSpot._get_ticker_normalize_function,
        )
        return path, {}, extra_data

    @staticmethod
    def _get_ticker_normalize_function(input_data, extra_data):
        if input_data is None:
            return [], False
        if isinstance(input_data, dict):
            return [
                BitsoRequestTickerData(
                    input_data,
                    extra_data["symbol_name"],
                    extra_data["asset_type"],
                    True,
                ),
            ], True
        return [], False

    def get_ticker(self, symbol, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_ticker(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def get_tick(self, symbol, extra_data=None, **kwargs) -> Any:
        return self.get_ticker(symbol, extra_data=extra_data, **kwargs)

    def async_get_ticker(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_ticker(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        self.async_get_ticker(symbol, extra_data=extra_data, **kwargs)

    def get_server_time(self, extra_data=None, **kwargs) -> Any:
        path = "/time"
        extra_data = update_extra_data(
            extra_data,
            request_type="get_server_time",
            symbol_name="ALL",
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=BitsoRequestData._extract_data_normalize_function,
        )
        return self.request(path, params={}, extra_data=extra_data)

    def _get_balance(self, extra_data=None, **kwargs) -> Any:
        path = "/balance"
        extra_data = update_extra_data(
            extra_data,
            request_type="get_balance",
            symbol_name="ALL",
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=BitsoRequestData._extract_data_normalize_function,
        )
        return path, {}, extra_data

    def get_balance(self, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_balance(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def get_account(self, symbol=None, extra_data=None, **kwargs) -> Any:
        return self.get_balance(extra_data=extra_data, **kwargs)

    def async_get_balance(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_balance(extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        request_symbol = self._params.get_symbol(symbol)
        side, otype = order_type.split("-") if "-" in order_type else (order_type, "limit")
        body = {
            "book": request_symbol,
            "side": side.lower(),
            "type": otype.lower(),
            "major": str(vol),
        }
        if price is not None:
            body["price"] = str(price)
        if client_order_id:
            body["client_id"] = str(client_order_id)
        extra_data = update_extra_data(
            extra_data,
            request_type="make_order",
            symbol_name=symbol,
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=BitsoRequestData._extract_data_normalize_function,
        )
        return "/orders", body, extra_data

    def make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, body, extra_data = self._make_order(
            symbol,
            vol,
            price,
            order_type,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, body=body, extra_data=extra_data)

    def async_make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, body, extra_data = self._make_order(
            symbol,
            vol,
            price,
            order_type,
            client_order_id,
            extra_data,
            **kwargs,
        )
        self.submit(
            self.async_request(path, body=body, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _cancel_order(
        self,
        symbol,
        order_id=None,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ) -> Any:
        body = {}
        if order_id:
            body["order_id"] = str(order_id)
        if client_order_id:
            body["client_id"] = str(client_order_id)
        extra_data = update_extra_data(
            extra_data,
            request_type="cancel_order",
            order_id=order_id or client_order_id,
            symbol_name=symbol,
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=None,
        )
        return "/orders", body, extra_data

    def cancel_order(self, symbol, order_id=None, client_order_id=None, extra_data=None, **kwargs):
        path, body, extra_data = self._cancel_order(
            symbol,
            order_id,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, body=body, extra_data=extra_data)

    def _get_depth(self, symbol, limit=100, extra_data=None, **kwargs) -> Any:
        request_symbol = self._params.get_symbol(symbol)
        path = f"/order_book?book={request_symbol}&aggregate={limit}"
        extra_data = update_extra_data(
            extra_data,
            request_type="get_depth",
            symbol_name=symbol,
            exchange_name=self.exchange_name,
            asset_type=self.asset_type,
            normalize_function=BitsoRequestData._extract_data_normalize_function,
        )
        return path, {}, extra_data

    def get_depth(self, symbol, limit=100, extra_data=None, **kwargs) -> Any:
        path, params, extra_data = self._get_depth(symbol, limit, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(self, symbol, limit=100, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(symbol, limit, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )
