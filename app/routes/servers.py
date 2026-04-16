from fastapi import APIRouter

from app.schemas import (
    RegisterServerRequest,
    RegisterServerResponse,
    RegisteredServer,
    UnregisterServerRequest,
    UnregisterServerResponse,
)
from app.services.server_service import ServerService

router = APIRouter(tags=["servers"])


@router.post("/register", response_model=RegisterServerResponse)
def register(payload: RegisterServerRequest) -> RegisterServerResponse:
    return ServerService.register_server(payload)


@router.get("/get_registered_servers", response_model=list[RegisteredServer])
def get_registered_servers(query: str | None = None) -> list[RegisteredServer]:
    servers = ServerService.get_registered_servers()

    if not query or not query.strip():
        return servers

    q = query.strip().lower()
    return [
        server
        for server in servers
        if q in server.service_id.lower()
        or q in server.ip.lower()
        or q in server.api_url.lower()
    ]


@router.post("/unregister", response_model=UnregisterServerResponse)
def unregister(payload: UnregisterServerRequest) -> UnregisterServerResponse:
    return ServerService.unregister_server(payload.service_id)
