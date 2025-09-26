from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.routers_injectors_service import routers
import uvicorn

from system_setup.db_connect import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.pool = await init_db()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan, title="Alarm Security System Agent", version="1.0.0")

# ---- Enable CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5218"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Add routers for all api ----
for router in routers:
    app.include_router(router)  

# ---- Entry point ----
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )