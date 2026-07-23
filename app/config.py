"""应用配置集中管理。"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_URL = f"sqlite:///{(PROJECT_ROOT / 'amazon_dashboard.db').as_posix()}"


def _positive_float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name, str(default))
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} 必须是数字") from exc
    if value <= 0:
        raise RuntimeError(f"{name} 必须大于 0")
    return value


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Amazon Seller AI Dashboard")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv(
        "DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"
    ).rstrip("/")
    usd_cny_rate: float = _positive_float_env("USD_CNY_RATE", 7.2)


settings = Settings()
