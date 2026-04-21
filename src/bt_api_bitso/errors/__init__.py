from bt_api_base.error import ErrorTranslator, UnifiedError, UnifiedErrorCode


class BitsoErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        100: (UnifiedErrorCode.INTERNAL_ERROR, "Generic error"),
        102: (UnifiedErrorCode.INVALID_PARAMETER, "Invalid parameter"),
        103: (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        104: (UnifiedErrorCode.INVALID_SIGNATURE, "Invalid signature"),
        105: (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded"),
        200: (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance"),
        204: (UnifiedErrorCode.INVALID_ORDER_TYPE, "Invalid order type"),
        205: (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        206: (UnifiedErrorCode.MIN_NOTIONAL, "Minimum notional not met"),
        300: (UnifiedErrorCode.INVALID_SYMBOL, "Invalid book"),
    }

    HTTP_STATUS_MAP = {
        400: (UnifiedErrorCode.INVALID_PARAMETER, "Bad request"),
        401: (UnifiedErrorCode.INVALID_API_KEY, "Unauthorized"),
        403: (UnifiedErrorCode.PERMISSION_DENIED, "Forbidden"),
        404: (UnifiedErrorCode.ORDER_NOT_FOUND, "Not found"),
        429: (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Too many requests"),
        500: (UnifiedErrorCode.INTERNAL_ERROR, "Internal server error"),
        503: (UnifiedErrorCode.EXCHANGE_OVERLOADED, "Service unavailable"),
    }

    @classmethod
    def translate(cls, raw_error: dict, venue: str) -> UnifiedError | None:
        error = raw_error.get("error", raw_error)
        code = error.get("code")
        msg = error.get("message", error.get("msg", ""))

        if code is not None and code in cls.ERROR_MAP:
            unified_code, default_msg = cls.ERROR_MAP[code]
            return UnifiedError(
                code=unified_code,
                category=cls._get_category(unified_code),
                venue=venue,
                message=msg or default_msg,
                original_error=f"{code}: {msg}",
                context={"raw_response": raw_error},
            )

        status = error.get("status")
        if status and status in cls.HTTP_STATUS_MAP:
            unified_code, default_msg = cls.HTTP_STATUS_MAP[status]
            return UnifiedError(
                code=unified_code,
                category=cls._get_category(unified_code),
                venue=venue,
                message=msg or default_msg,
                original_error=f"HTTP {status}: {msg}",
                context={"raw_response": raw_error},
            )

        return UnifiedError(
            code=UnifiedErrorCode.INTERNAL_ERROR,
            category=cls._get_category(UnifiedErrorCode.INTERNAL_ERROR),
            venue=venue,
            message=msg or "Unknown error",
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
