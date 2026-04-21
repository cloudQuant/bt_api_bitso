# BITSO Documentation

## English

Welcome to the BITSO documentation for bt_api.

### Quick Start

```bash
pip install bt_api_bitso
```

```python
from bt_api_bitso import BitsoApi
feed = BitsoApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## 中文

欢迎使用 bt_api 的 BITSO 文档。

### 快速开始

```bash
pip install bt_api_bitso
```

```python
from bt_api_bitso import BitsoApi
feed = BitsoApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## API Reference

See source code in `src/bt_api_bitso/` for detailed API documentation.
