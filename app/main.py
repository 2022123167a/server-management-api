try:
    from app.routes.metrics import router as metrics_router
    from app.routes.servers import router as servers_router
except ModuleNotFoundError:
    from routes.metrics import router as metrics_router
    from routes.servers import router as servers_router

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI(
    title="Server Management API",
    version="1.0.0",
)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.include_router(servers_router)
app.include_router(metrics_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=False)
