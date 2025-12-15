from fastapi import FastAPI
from app.router.user_route import user_router
from app.router.project_route import project_router
from app.database.core import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print("DB connection failed:", e)


app.include_router(router=project_router, prefix="", tags=["projects"])