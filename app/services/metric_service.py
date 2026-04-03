from datetime import UTC, datetime, timedelta

from app.db import metrics_master
from app.models import MetricRecord
from app.schemas import (
    BlockMetricRequest,
    MetricData,
    MetricOperationResponse,
    MetricOperationResult,
    UnblockMetricRequest,
)


class MetricService:
    @staticmethod
    def get_metrics() -> list[MetricData]:
        MetricService._refresh_metric_statuses()
        return [
            MetricData.model_validate(metric)
            for metric in sorted(metrics_master.values(), key=lambda item: (item.api_source, item.metric_name))
        ]

    @staticmethod
    def block_metrics(payload: BlockMetricRequest) -> MetricOperationResponse:
        MetricService._refresh_metric_statuses()
        blocked_until = datetime.now(UTC) + timedelta(seconds=payload.block_seconds)
        results: list[MetricOperationResult] = []

        for metric_name in payload.metrics:
            metric = MetricService._get_or_create_metric(metric_name, payload.api_source)
            metric.is_active = 0
            metric.blocked_until = blocked_until
            results.append(
                MetricOperationResult(
                    metric_name=metric.metric_name,
                    api_source=metric.api_source,
                    status="blocked",
                )
            )

        return MetricOperationResponse(status="success", results=results)

    @staticmethod
    def unblock_metrics(payload: UnblockMetricRequest) -> MetricOperationResponse:
        MetricService._refresh_metric_statuses()
        results: list[MetricOperationResult] = []

        for metric_name in payload.metrics:
            metric = MetricService._get_or_create_metric(metric_name, payload.api_source)
            metric.is_active = 1
            metric.blocked_until = None
            results.append(
                MetricOperationResult(
                    metric_name=metric.metric_name,
                    api_source=metric.api_source,
                    status="active",
                )
            )

        return MetricOperationResponse(status="success", results=results)

    @staticmethod
    def _get_or_create_metric(metric_name: str, api_source: str) -> MetricRecord:
        key = (metric_name, api_source)
        metric = metrics_master.get(key)
        if metric is None:
            metric = MetricRecord(
                metric_name=metric_name,
                is_active=1,
                api_source=api_source,
            )
            metrics_master[key] = metric
        return metric

    @staticmethod
    def _refresh_metric_statuses() -> None:
        now = datetime.now(UTC)
        for metric in metrics_master.values():
            if metric.blocked_until and metric.blocked_until <= now:
                metric.is_active = 1
                metric.blocked_until = None
