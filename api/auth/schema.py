# -*- coding: utf-8 -*-
from pydantic import BaseModel


class RequestAuthLogin(BaseModel):
    email: str
    password: str

    def is_valid(self, expected_email: str, expected_password: str) -> bool:
        """
        Check if the provided email and password match the expected values.
        """
        if not isinstance(expected_email, str) or not isinstance(expected_password, str):
            return False
        return (
            self.email.strip().lower() == expected_email.lower() 
            and self.password.strip().lower() == expected_password.lower()
        )