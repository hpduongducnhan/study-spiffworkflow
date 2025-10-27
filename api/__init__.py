# -*- coding: utf-8 -*-
from fastapi import APIRouter
from .bpm_workflow import bpm_workflow_router
from .auth import auth_router


api_router = APIRouter(prefix="/api")
for r in [bpm_workflow_router, auth_router]:
    api_router.include_router(r)
