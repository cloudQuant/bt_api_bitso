# Bitso Exchange Plugin for bt_api

## Bitso | 比特索

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitso.svg)](https://pypi.org/project/bt_api_bitso/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitso.svg)](https://pypi.org/project/bt_api_bitso/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitso/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitso/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitso/badge/?version=latest)](https://bt-api-bitso.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

This package provides **Bitso exchange plugin** for the [bt_api](https://github.com/cloudQuant/bt_api_py) framework. It offers a unified interface for interacting with **Bitso**, the largest cryptocurrency exchange in Latin America.

Bitso provides trading in Mexican Peso (MXN), USD, BTC, ETH, and other digital assets. This plugin integrates Bitso's REST API v3 into the bt_api unified trading framework.

### Key Features

- **Complete REST API Coverage**: Ticker, order book, klines, trades, orders, balances
- **HMAC-SHA256 Authentication**: Secure API key and secret key authentication
- **Rate Limit Protection**: Built-in rate limiter (60 requests/second per IP)
- **Unified Interface**: Compatible with bt_api's BtApi, EventBus, and data containers
- **Async Support**: Full async/await support for concurrent operations

### Exchange Information

| Item | Value |
|------|-------|
| Exchange Name | Bitso |
| Trading Code | `BITSO___SPOT` |
| REST API URL | `https://bitso.com/api/v3` |
| WebSocket URL | `wss://ws.bitso.com` |
| Asset Type | SPOT |
| Supported Currencies | MXN, USD, BTC, ETH, USDC |
| Rate Limit | 60 requests/second per IP |
| Authentication | Bearer Token + HMAC-SHA256 |

### Installation

#### From PyPI (Recommended)

```bash
pip install bt_api_bitso
```

#### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitso
cd bt_api_bitso
pip install -e .
```

### Quick Start

#### Initialize the Exchange

```python
from bt_api_py import BtApi

# Configure Bitso exchange
exchange_config = {
    "BITSO___SPOT": {
        "api_key": "your_api_key",
        "secret_key": "your_secret_key",
    }
}

# Initialize BtApi
api = BtApi(exchange_kwargs=exchange_config)
```

#### Get Market Data

```python
# Get ticker
ticker = api.get_tick("BITSO___SPOT", "BTC/MXN")
print(ticker)

# Get order book depth
depth = api.get_depth("BITSO___SPOT", "BTC/MXN", limit=20)
print(depth)

# Get kline/candlestick data
klines = api.get_kline("BITSO___SPOT", "BTC/MXN", period="1h", count=100)
print(klines)

# Get recent trades
trades = api.get_trades("BITSO___SPOT", "BTC/MXN")
print(trades)
```

#### Trading Operations

```python
# Place an order
order = api.make_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    volume=0.01,
    price=500000,
    order_type="buy-limit",
)
print(order)

# Cancel an order
cancel_result = api.cancel_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    order_id="your_order_id",
)
print(cancel_result)

# Query order status
order_info = api.query_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    order_id="your_order_id",
)
print(order_info)

# Get open orders
open_orders = api.get_open_orders("BITSO___SPOT", "BTC/MXN")
print(open_orders)

# Get account balance
balance = api.get_balance("BITSO___SPOT")
print(balance)
```

#### Asynchronous Operations

```python
import asyncio
from bt_api_py import BtApi

async def main():
    api = BtApi(exchange_kwargs={
        "BITSO___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret_key",
        }
    })

    # Async get ticker
    ticker = await api.async_get_tick("BITSO___SPOT", "BTC/MXN")
    print(ticker)

    # Async place order
    order = await api.async_make_order(
        exchange_name="BITSO___SPOT",
        symbol="BTC/MXN",
        volume=0.01,
        price=500000,
        order_type="buy-limit",
    )
    print(order)

asyncio.run(main())
```

### Supported Operations

| Operation | REST API | Description |
|-----------|----------|-------------|
| `get_tick` | GET /ticker | Get ticker data (last price, volume, etc.) |
| `get_depth` | GET /order_book | Get order book depth |
| `get_kline` | GET /ohlc | Get candlestick/kline data |
| `get_trades` | GET /trades | Get recent trades |
| `make_order` | POST /orders | Place a new order |
| `cancel_order` | DELETE /orders | Cancel an order |
| `query_order` | GET /orders | Query order status |
| `get_open_orders` | GET /open_orders | Get all open orders |
| `get_deals` | GET /user_trades | Get user trade history |
| `get_balance` | GET /balance | Get account balance |
| `get_account` | GET /balance | Get account information |
| `get_server_time` | GET /time | Get server time |
| `get_exchange_info` | GET /available_books | Get available trading pairs |

### Symbol Format

Bitso uses lowercase symbols with underscore separator:

| bt_api Symbol | Bitso Symbol |
|---------------|--------------|
| `BTC/MXN` | `btc_mxn` |
| `ETH/MXN` | `eth_mxn` |
| `XRP/MXN` | `xrp_mxn` |
| `BTC/USD` | `btc_usd` |

The plugin automatically converts between formats.

### Order Types

Bitso supports the following order types:

| Order Type | Description |
|------------|-------------|
| `buy-limit` | Buy limit order |
| `sell-limit` | Sell limit order |
| `buy-market` | Buy market order |
| `sell-market` | Sell market order |

### Rate Limiting

Bitso implements a rate limit of **60 requests per second** per IP address. This plugin includes a built-in rate limiter using sliding window algorithm to prevent exceeding the limit.

### Error Handling

All API errors are translated to bt_api's standard error types:

```python
from bt_api_py.errors import (
    RateLimitError,
    AuthenticationError,
    OrderNotFoundError,
    InsufficientBalanceError,
)
```

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitso.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitso.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitso |
| Bitso API Docs | https://bitso.com/api/v3 |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitso/issues |

### Architecture

```
bt_api_bitso/
├── src/bt_api_bitso/           # Source code
│   ├── containers/              # Data containers
│   │   ├── balances/           # Balance data containers
│   │   └── orders/             # Order data containers
│   ├── exchange_data/          # Exchange configuration
│   │   └── __init__.py         # BitsoExchangeData class
│   ├── feeds/                  # API feeds
│   │   └── live_bitso/         # Live trading feed
│   │       ├── __init__.py     # BitsoRequestData base class
│   │       └── spot.py         # Spot trading feed
│   ├── tickers/                # Ticker data containers
│   ├── errors/                 # Error translations
│   └── plugin.py               # Plugin registration
├── tests/                      # Unit tests
└── docs/                       # Documentation
```

### Requirements

| Dependency | Version | Description |
|------------|---------|-------------|
| Python | >= 3.9 | Programming language |
| bt_api_base | >= 0.15 | Core framework |

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

MIT License - see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitso/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitso（比特索）交易所插件**。Bitso 是拉丁美洲最大的加密货币交易所，提供墨西哥比索（MXN）、美元（USD）、比特币（BTC）、以太坊（ETH）和其他数字资产的交易服务。

本插件将 Bitso 的 REST API v3 集成到 bt_api 统一交易框架中，提供标准化的行情查询、订单管理和账户查询接口。

### 核心功能

- **完整 REST API 覆盖**：行情、订单簿、K线、交易、订单、余额
- **HMAC-SHA256 认证**：安全的 API Key 和 Secret Key 认证
- **速率限制保护**：内置限流器（每秒 60 请求/IP）
- **统一接口**：与 bt_api 的 BtApi、EventBus 和数据容器完全兼容
- **异步支持**：完整的 async/await 支持并发操作

### 交易所信息

| 项目 | 值 |
|------|-------|
| 交易所名称 | Bitso（比特索） |
| 交易代码 | `BITSO___SPOT` |
| REST API 地址 | `https://bitso.com/api/v3` |
| WebSocket 地址 | `wss://ws.bitso.com` |
| 资产类型 | 现货（SPOT） |
| 支持法币 | MXN, USD, BTC, ETH, USDC |
| 速率限制 | 每秒 60 请求/IP |
| 认证方式 | Bearer Token + HMAC-SHA256 |

### 安装

#### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitso
```

#### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitso
cd bt_api_bitso
pip install -e .
```

### 快速开始

#### 初始化交易所

```python
from bt_api_py import BtApi

# 配置 Bitso 交易所
exchange_config = {
    "BITSO___SPOT": {
        "api_key": "your_api_key",
        "secret_key": "your_secret_key",
    }
}

# 初始化 BtApi
api = BtApi(exchange_kwargs=exchange_config)
```

#### 获取市场数据

```python
# 获取行情
ticker = api.get_tick("BITSO___SPOT", "BTC/MXN")
print(ticker)

# 获取订单簿深度
depth = api.get_depth("BITSO___SPOT", "BTC/MXN", limit=20)
print(depth)

# 获取 K 线数据
klines = api.get_kline("BITSO___SPOT", "BTC/MXN", period="1h", count=100)
print(klines)

# 获取最近交易
trades = api.get_trades("BITSO___SPOT", "BTC/MXN")
print(trades)
```

#### 交易操作

```python
# 下单
order = api.make_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    volume=0.01,
    price=500000,
    order_type="buy-limit",
)
print(order)

# 取消订单
cancel_result = api.cancel_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    order_id="your_order_id",
)
print(cancel_result)

# 查询订单状态
order_info = api.query_order(
    exchange_name="BITSO___SPOT",
    symbol="BTC/MXN",
    order_id="your_order_id",
)
print(order_info)

# 获取挂单
open_orders = api.get_open_orders("BITSO___SPOT", "BTC/MXN")
print(open_orders)

# 获取账户余额
balance = api.get_balance("BITSO___SPOT")
print(balance)
```

#### 异步操作

```python
import asyncio
from bt_api_py import BtApi

async def main():
    api = BtApi(exchange_kwargs={
        "BITSO___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret_key",
        }
    })

    # 异步获取行情
    ticker = await api.async_get_tick("BITSO___SPOT", "BTC/MXN")
    print(ticker)

    # 异步下单
    order = await api.async_make_order(
        exchange_name="BITSO___SPOT",
        symbol="BTC/MXN",
        volume=0.01,
        price=500000,
        order_type="buy-limit",
    )
    print(order)

asyncio.run(main())
```

### 支持的操作

| 操作 | REST API | 说明 |
|------|----------|------|
| `get_tick` | GET /ticker | 获取行情数据（最新价格、成交量等） |
| `get_depth` | GET /order_book | 获取订单簿深度 |
| `get_kline` | GET /ohlc | 获取 K 线/蜡烛图数据 |
| `get_trades` | GET /trades | 获取最近交易 |
| `make_order` | POST /orders | 下新订单 |
| `cancel_order` | DELETE /orders | 取消订单 |
| `query_order` | GET /orders | 查询订单状态 |
| `get_open_orders` | GET /open_orders | 获取所有挂单 |
| `get_deals` | GET /user_trades | 获取用户交易历史 |
| `get_balance` | GET /balance | 获取账户余额 |
| `get_account` | GET /balance | 获取账户信息 |
| `get_server_time` | GET /time | 获取服务器时间 |
| `get_exchange_info` | GET /available_books | 获取可交易交易对 |

### 交易对格式

Bitso 使用小写字母加下划线分隔符的格式：

| bt_api 交易对 | Bitso 交易对 |
|---------------|--------------|
| `BTC/MXN` | `btc_mxn` |
| `ETH/MXN` | `eth_mxn` |
| `XRP/MXN` | `xrp_mxn` |
| `BTC/USD` | `btc_usd` |

插件会自动转换格式。

### 订单类型

Bitso 支持以下订单类型：

| 订单类型 | 说明 |
|----------|------|
| `buy-limit` | 买入限价单 |
| `sell-limit` | 卖出限价单 |
| `buy-market` | 买入市价单 |
| `sell-market` | 卖出市价单 |

### 速率限制

Bitso 的速率限制为 **每秒 60 请求**（每个 IP 地址）。本插件内置了滑动窗口算法的限流器，防止超出限制。

### 错误处理

所有 API 错误都会转换为 bt_api 的标准错误类型：

```python
from bt_api_py.errors import (
    RateLimitError,          # 速率限制错误
    AuthenticationError,     # 认证错误
    OrderNotFoundError,      # 订单未找到
    InsufficientBalanceError,  # 余额不足
)
```

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitso.readthedocs.io/ |
| 中文文档 | https://bt-api-bitso.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitso |
| Bitso API 文档 | https://bitso.com/api/v3 |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitso/issues |

### 系统要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.9 | 编程语言 |
| bt_api_base | >= 0.15 | 核心框架 |

### 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitso/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com

---

如果这个项目对您有帮助，请给我们一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=cloudQuant/bt_api_bitso&type=Date)](https://star-history.com/#cloudQuant/bt_api_bitso&Date)
