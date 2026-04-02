"""One JSON object per line — easy to ship to Loki, Cloud Logging, etc."""

from __future__ import annotations

import json
import logging
from typing import Any

_logger = logging.getLogger("ai_interview_simulator")


def log_event(event: str, **fields: Any) -> None:
    from app.observability.context import request_id_var

    rid = request_id_var.get()
    payload = {"event": event, **fields}
    if rid:
        payload["request_id"] = rid
    _logger.info(json.dumps(payload, default=str))
