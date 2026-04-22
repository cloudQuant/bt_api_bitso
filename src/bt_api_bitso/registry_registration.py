from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import nested_balance_handler as _bitso_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitso.exchange_data import BitsoExchangeData
from bt_api_bitso.feeds.live_bitso.spot import BitsoRequestDataSpot


def _bitso_spot_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any,
) -> None:
    topic_list = [i["topic"] for i in topics]
    bt_api.log(f"Bitso Spot topics requested: {topic_list}")


def register_bitso(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("BITSO___SPOT", BitsoRequestDataSpot)
    registry.register_exchange_data("BITSO___SPOT", BitsoExchangeData)
    registry.register_balance_handler("BITSO___SPOT", _bitso_balance_handler)
    registry.register_stream("BITSO___SPOT", "subscribe", _bitso_spot_subscribe_handler)
