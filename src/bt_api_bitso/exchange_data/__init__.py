from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BitsoExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITSO___SPOT"
        self.rest_url = "https://bitso.com/api/v3"
        self.wss_url = "wss://ws.bitso.com"
        self.rest_paths = {
            "ping": "GET /ping",
            "get_server_time": "GET /time",
            "get_exchange_info": "GET /available_books",
            "get_tick": "GET /ticker",
            "get_depth": "GET /order_book",
            "get_kline": "GET /ohlc",
            "get_trades": "GET /trades",
            "get_account": "GET /balance",
            "get_balance": "GET /balance",
            "make_order": "POST /orders",
            "cancel_order": "DELETE /orders",
            "cancel_all_orders": "DELETE /orders/all",
            "query_order": "GET /orders",
            "get_open_orders": "GET /open_orders",
            "get_deals": "GET /user_trades",
        }
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "60",
            "3m": "180",
            "5m": "300",
            "15m": "900",
            "30m": "1800",
            "1h": "3600",
            "2h": "7200",
            "4h": "14400",
            "6h": "21600",
            "12h": "43200",
            "1d": "86400",
            "3d": "259200",
        }
        self.legal_currency = ["MXN", "USD", "BTC", "ETH", "USDC"]
        self.asset_type = "SPOT"
        self.status_dict = {}
        self.rate_limit_type = "sliding_window"
        self.interval = "1"
        self.limit = 60
        self.rate_limits = []
        self.server_time = 0.0
        self.local_update_time = 0.0
        self.timezone = "UTC"

    def get_symbol(self, symbol: str) -> str:
        return symbol.replace("/", "_").replace("-", "_").lower()

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]

    def get_wss_path(self, channel: str, symbol: str | None = None, **kwargs) -> str:
        tpl = self.wss_paths.get(channel, "")
        if symbol and tpl:
            book = self.get_symbol(symbol)
            return tpl.replace("{book}", book)
        return tpl

    def get_symbol_path(self, symbol: str) -> str:
        return self.get_symbol(symbol)

    def get_instrument_name(self, symbol: str) -> str:
        return self.get_symbol(symbol)

    def get_symbol_from_instrument(self, instrument_name: str) -> str:
        parts = instrument_name.split("_")
        return f"{parts[0].upper()}/{parts[1].upper()}" if len(parts) == 2 else instrument_name

    def validate_symbol(self, symbol: str) -> bool:
        if not symbol:
            return False
        return True

    def get_depth_levels(self, depth: int = 50) -> int:
        return min(max(1, depth), 100)

    def get_kline_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_period_from_kline(self, kline_period: str) -> str:
        reverse_map = {v: k for k, v in self.kline_periods.items()}
        return reverse_map.get(kline_period, kline_period)
