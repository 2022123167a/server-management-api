from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.db import registered_servers
from app.models import ServerRecord
from app.schemas import (
    RegisterServerRequest,
    RegisterServerResponse,
    RegisteredServer,
    UnregisterServerResponse,
)


class ServerService:
    @staticmethod
    def register_server(payload: RegisterServerRequest) -> RegisterServerResponse:
        now = datetime.now(UTC).isoformat()
        existing_server = registered_servers.get(payload.service_id)

        if existing_server:
            existing_server.ip = payload.ip
            existing_server.api_url = payload.api_url
            existing_server.is_active = 1
            existing_server.retry_level = 0
            existing_server.last_metric_time = now
            existing_server.updated_at = now
        else:
            registered_servers[payload.service_id] = ServerRecord(
                service_id=payload.service_id,
                ip=payload.ip,
                api_url=payload.api_url,
                is_active=1,
                retry_level=0,
                last_metric_time=now,
                updated_at=now,
            )

        return RegisterServerResponse(
            status="registered",
            service=payload.service_id,
            ip=payload.ip,
            api_url=payload.api_url,
        )

    @staticmethod
    def get_registered_servers() -> list[RegisteredServer]:
        return [
            RegisteredServer.model_validate(server)
            for server in sorted(registered_servers.values(), key=lambda item: item.service_id)
        ]

    @staticmethod
    def unregister_server(service_id: str) -> UnregisterServerResponse:
        deleted_server = registered_servers.pop(service_id, None)
        if deleted_server is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{service_id} servisi bulunamadi.",
            )

        return UnregisterServerResponse(status="unregistered", service=service_id)
