from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ServerRecord:
    service_id: str
    ip: str
    api_url: str
    is_active: int
    retry_level: int
    last_metric_time: str
    updated_at: str


@dataclass
class MetricRecord:
    metric_name: str
    is_active: int
    api_source: str
    blocked_until: Optional[datetime] = None
