# bt_api_bitso

Bitso exchange plugin for `bt_api`.

## Installation

```bash
pip install bt_api_bitso
```

## Usage

```python
from bt_api_bitso import BitsoRequestDataSpot

feed = BitsoRequestDataSpot(public_key="your_key", private_key="your_secret")
ticker = feed.get_ticker("BTCUSD")
```