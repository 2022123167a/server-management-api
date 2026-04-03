from fastapi import APIRouter

from app.schemas import (
    BlockMetricRequest,
    MetricData,
    MetricOperationResponse,
    UnblockMetricRequest,
)
from app.services.metric_service import MetricService

router = APIRouter(tags=["metrics"])


@router.get("/metrics_master", response_model=list[MetricData])
def metrics_master() -> list[MetricData]:
    return MetricService.get_metrics()


@router.post("/metrics_block", response_model=MetricOperationResponse)
def metrics_block(payload: BlockMetricRequest) -> MetricOperationResponse:
    return MetricService.block_metrics(payload)


@router.post("/metrics_unblock", response_model=MetricOperationResponse)
def metrics_unblock(payload: UnblockMetricRequest) -> MetricOperationResponse:
    return MetricService.unblock_metrics(payload)
