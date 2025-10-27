# -*- coding: utf-8 -*-
from .router import api_router
from .schema import RequestAuthLogin


@api_router.post("/login", response_model=dict)
async def login(rbody: RequestAuthLogin):
    if rbody.is_valid("nhandd3@fpt.com", "password"):
        return {
            "message": "Login successful",
            "data": {
                "user": {
                    "email": rbody.email,
                },
                "access_token": "fake_access_token",
                "token_type": "bearer",
                "refresh_token": "fake_refresh_token",
                "expires_in": 3600,
            }
        }
    return {
        "message": "Invalid email or password",
    }