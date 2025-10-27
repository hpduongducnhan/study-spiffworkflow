# -*- coding: utf-8 -*-
from fastapi import APIRouter

api_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(verify_basic_credentials)],
)


