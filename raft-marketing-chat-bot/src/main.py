from fastapi import FastAPI
from api.v1.routers import router as routers_v1
from api.routers import router as routers


app = FastAPI()

app.include_router(routers)
app.include_router(routers_v1, prefix="/v1")
