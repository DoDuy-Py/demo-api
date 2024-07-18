# app/main.py

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from views import water_quality
from views import router
from shared_func.loop_func import init_schedule
from shared_func.views_func import init_db

from core.settings import settings

import threading

# app = FastAPI(
#     # title=settings.PROJECT_NAME
# )

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, docs_url="/docs", redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        version=settings.VERSION,
        description='''
        Base frame with FastAPI micro framework + Postgresql
            - Login/Register with JWT
            - Permission
            - CRUD User
            - by duyy.dv@gmail.com
        '''
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    # application.include_router(router.router, prefix=settings.API_PREFIX)
    application.include_router(router.router, prefix="/api/v1", tags=["api-url"])
    # application.add_exception_handler(CustomException, http_exception_handler)
    application.mount("/static", StaticFiles(directory="static"), name="static")
    # application.mount("/media", StaticFiles(directory="media"), name="media")

    return application


app = get_application()

# app.include_router(router.router, prefix="/api/v1", tags=["api-url"])

#### LOOP DATA ####
threading.Thread(target=init_schedule).start()
threading.Thread(target=init_db).start()
# init_schedule()