from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logger import logger

async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception(f"An error occured error : {exc}")
        return JSONResponse(status_code=500, content={"message": "An internal server error occurred."})