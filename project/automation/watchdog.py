from __future__ import annotations

import psutil
import structlog

log = structlog.get_logger(__name__)


def check_process(name: str) -> bool:
    return any(name in (proc.info.get("name") or "") for proc in psutil.process_iter(["name"]))


def watchdog_tick() -> dict[str, bool]:
    status = {
        "telegram": check_process("Telegram"),
        "xvfb": check_process("Xvfb"),
        "celery": check_process("celery"),
    }
    log.info("watchdog_tick", **status)
    return status
