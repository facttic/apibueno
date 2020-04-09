"""
app.main.py
"""
import logging
import os

import pydantic
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .data import data_source
from .router.v1 import V1
from .router.v2 import V2
from .utils.httputils import setup_client_session, teardown_client_session

# ############
# FastAPI App
# ############
LOGGER = logging.getLogger("api")

APP = FastAPI(
    title="Argentina Covid19 API",
    description=(
        "API para el seguimiento del coronavirus en Argentina."
        " Project page: https://github.com/facttic/apibueno"
    ),
    version="0.0.1",
    docs_url="/",
    redoc_url="/docs",
    on_startup=[setup_client_session],
    on_shutdown=[teardown_client_session],
)

# #####################
# Middleware
#######################

# Enable CORS.
APP.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


@APP.middleware("http")
async def add_datasource(request: Request, call_next):
    """
    Attach the data source to the request.state.
    """
    # Retrieve the datas ource from query param.
    source = data_source(request.query_params.get("source", default="local"))

    # Abort with 404 if source cannot be found.
    if not source:
        return Response("La fuente de datos no se encontro.", status_code=404)

    # Attach source to request.
    request.state.source = source

    # Move on...
    LOGGER.info(f"source provided: {source.__class__.__name__}")
    response = await call_next(request)
    return response


# ################
# Exception Handler
# ################


@APP.exception_handler(pydantic.error_wrappers.ValidationError)
async def handle_validation_error(
    request: Request, exc: pydantic.error_wrappers.ValidationError
):  # pylint: disable=unused-argument
    """
    Handles validation errors.
    """
    return JSONResponse({"message": exc.errors()}, status_code=422)


# ################
# Routing
# ################


# Include routers.
APP.include_router(V1, prefix="", tags=["v1"])
APP.include_router(V2, prefix="/v2", tags=["v2"])


# Running of app.
if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP", host="127.0.0.1", port=int(os.getenv("PORT", "5000")), log_level="info",
    )
