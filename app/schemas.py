from pydantic import BaseModel, ConfigDict, Field


class RegisterServerRequest(BaseModel):
    service_id: str = Field(..., min_length=1)
    ip: str = Field(..., min_length=1)
    api_url: str = Field(..., min_length=1)


class RegisterServerResponse(BaseModel):
    status: str
    service: str
    ip: str
    api_url: str


class RegisteredServer(BaseModel):
    service_id: str
    ip: str
    api_url: str
    is_active: int
    retry_level: int
    last_metric_time: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class UnregisterServerRequest(BaseModel):
    service_id: str = Field(..., min_length=1)


class UnregisterServerResponse(BaseModel):
    status: str
    service: str


class MetricData(BaseModel):
    metric_name: str
    is_active: int
    api_source: str

    model_config = ConfigDict(from_attributes=True)


class BlockMetricRequest(BaseModel):
    metrics: list[str] = Field(..., min_length=1)
    block_seconds: int = Field(..., gt=0)
    api_source: str = Field(..., min_length=1)


class UnblockMetricRequest(BaseModel):
    metrics: list[str] = Field(..., min_length=1)
    api_source: str = Field(..., min_length=1)


class MetricOperationResult(BaseModel):
    metric_name: str
    api_source: str
    status: str


class MetricOperationResponse(BaseModel):
    status: str
    results: list[MetricOperationResult]
