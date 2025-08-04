"""Logging system with CallContext support."""

import contextvars
import json
import logging
import re
import sys
from typing import Optional

from model_router.domain.call_context import CallContext

current_context: contextvars.ContextVar[CallContext | None] = contextvars.ContextVar(
    "call_context",
    default=None
)


def get_system_call_context(name: str = 'system') -> CallContext:
    """Get system call context."""
    return CallContext(user_id=name)


def get_no_auth_call_context() -> CallContext:
    """Get no-auth call context."""
    return CallContext(user_id='no_auth')


class CallContextFilter(logging.Filter):
    """Filter that adds CallContext information to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        ctx: CallContext | None = current_context.get()

        if ctx:
            record.user_id = ctx.user_id or 'N/A'
            record.request_id = ctx.request_id or 'null'
        else:
            record.user_id = 'N/A'
            record.request_id = 'null'

        record.log_level = record.levelname
        return True


COLORS = {
    'DEBUG': "\033[94m",  # Blue
    'INFO': "\033[92m",  # Green
    'WARNING': "\033[93m",  # Yellow
    'ERROR': "\033[91m",  # Red
    'CRITICAL': "\033[95m",  # Magenta
}
RESET = "\033[0m"
GRAY = "\033[90m"


class ContextualLoggingAdapter(logging.LoggerAdapter):
    """Logging adapter that supports CallContext."""

    def __init__(self, logger: logging.Logger):
        super().__init__(logger, extra={})

    def process(self, msg, kwargs):
        # If caller passed `call_context=some_CallContext`, override the ContextVar
        ctx_override: CallContext | None = kwargs.pop("call_context", None)
        if ctx_override is not None:
            current_context.set(ctx_override)
        return msg, kwargs


class ColoredFormatter(logging.Formatter):
    """Formatter with colors and JSON prettification."""

    def format(self, record):
        # Colorize levelname
        level_color = COLORS.get(record.levelname, "")
        record.levelname = f"{level_color}{record.levelname}{RESET}"

        # Pretty-print embedded JSON-like string
        message = str(record.getMessage())
        match = re.search(r"({.*})", message)
        if match:
            raw_dict_str = match.group(1)
            try:
                # Try to parse as JSON first
                parsed_dict = json.loads(raw_dict_str)
                pretty_json = json.dumps(parsed_dict, indent=2, ensure_ascii=False)
                message = message.replace(raw_dict_str, f"\n{pretty_json}")
            except (ValueError, json.JSONDecodeError):
                try:
                    # Fall back to ast.literal_eval
                    import ast
                    parsed_dict = ast.literal_eval(raw_dict_str)
                    pretty_json = json.dumps(parsed_dict, indent=2, ensure_ascii=False)
                    message = message.replace(raw_dict_str, f"\n{pretty_json}")
                except (ValueError, SyntaxError):
                    pass  # Leave message as-is if parsing fails

        record.msg = message
        return super().format(record)


def get_logger(name: str) -> logging.LoggerAdapter:
    """Get a logger with CallContext support."""
    root = logging.getLogger(name)
    root.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplication
    if root.handlers:
        root.handlers.clear()

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)

    # Use colored formatter for development
    formatter = ColoredFormatter(
        '%(levelname)s - [%(funcName)s] |user_id: %(user_id)s|req_id: %(request_id)s| %(message)s'
    )
    stdout_handler.setFormatter(formatter)

    root.addHandler(stdout_handler)
    root.addFilter(CallContextFilter())

    adapter = ContextualLoggingAdapter(root)
    return adapter
