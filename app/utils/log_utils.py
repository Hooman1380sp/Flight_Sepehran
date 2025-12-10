import logging
import json
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from functools import lru_cache


@lru_cache(maxsize=1)
def get_logger(name: str = "app_logger", filename: str = "app.log"):
    logs_dir = Path("app/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            logs_dir / filename,
            maxBytes=5_000_000,
            backupCount=5)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    return logger


def log_change(entity: str, entity_id: int, diffs: dict, actor: str = "system"):
    logger = get_logger(
        name=f"{entity}_logger",
        filename=f"{entity}_changes.log")

    payload = {
        "entity": entity,
        "id": entity_id,
        "changed_at": datetime.utcnow().isoformat(),
        "changed_by": actor,
        "diffs": diffs}

    logger.info(json.dumps(payload, default=str))
