import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.project_config import settings
from config.database.db_helper import db_helper
from routers.product import router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION
    )


    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router)

    @application.on_event("startup")
    async def startup_db():
        session = db_helper.get_scope_session()
        application.state.db = session
        try:
            yield session
        finally:
            session.remove()

    @application.on_event("shutdown")
    async def shutdown_db():
        await db_helper.engine.dispose()

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)