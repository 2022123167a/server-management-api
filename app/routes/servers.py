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
def get_registered_servers() -> list[RegisteredServer]:
    return ServerService.get_registered_servers()


@router.post("/unregister", response_model=UnregisterServerResponse)
def unregister(payload: UnregisterServerRequest) -> UnregisterServerResponse:
    return ServerService.unregister_server(payload.service_id)
