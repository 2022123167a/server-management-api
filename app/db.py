from datetime import UTC, datetime, timedelta

from app.models import MetricRecord, ServerRecord


def _iso_datetime(minutes_ago: int) -> str:
    return (datetime.now(UTC) - timedelta(minutes=minutes_ago)).isoformat()


registered_servers: dict[str, ServerRecord] = {
    "auth-service": ServerRecord(
        service_id="auth-service",
        ip="10.20.1.15",
        api_url="http://10.20.1.15:9001",
        is_active=1,
        retry_level=0,
        last_metric_time=_iso_datetime(2),
        updated_at=_iso_datetime(1),
    ),
    "billing-service": ServerRecord(
        service_id="billing-service",
        ip="10.20.1.24",
        api_url="http://10.20.1.24:9010",
        is_active=0,
        retry_level=2,
        last_metric_time=_iso_datetime(18),
        updated_at=_iso_datetime(5),
    ),
    "inventory-service": ServerRecord(
        service_id="inventory-service",
        ip="10.20.1.39",
        api_url="http://10.20.1.39:9025",
        is_active=1,
        retry_level=1,
        last_metric_time=_iso_datetime(4),
        updated_at=_iso_datetime(3),
    ),
}

metrics_master: dict[tuple[str, str], MetricRecord] = {
    ("cpu_usage", "system-agent"): MetricRecord(
        metric_name="cpu_usage",
        is_active=1,
        api_source="system-agent",
    ),
    ("memory_usage", "system-agent"): MetricRecord(
        metric_name="memory_usage",
        is_active=1,
        api_source="system-agent",
    ),
    ("disk_usage", "system-agent"): MetricRecord(
        metric_name="disk_usage",
        is_active=0,
        api_source="system-agent",
        blocked_until=datetime.now(UTC) + timedelta(minutes=12),
    ),
    ("http_latency", "gateway-agent"): MetricRecord(
        metric_name="http_latency",
        is_active=1,
        api_source="gateway-agent",
    ),
    ("error_rate", "gateway-agent"): MetricRecord(
        metric_name="error_rate",
        is_active=1,
        api_source="gateway-agent",
    ),
}
