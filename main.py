from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from system_setup.env_setup import set_env
from services.routers_injectors_service import routers
import uvicorn

# ---- Set env ----
set_env()
app = FastAPI(title="Alarm Security System Agent", version="1.0.0")

# ---- Enable CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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