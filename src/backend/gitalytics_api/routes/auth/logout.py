#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import fastapi
from gitalytics_api.cookies import EncryptedCookieStorage
from gitalytics_api.enums import CookieKey


router = fastapi.APIRouter()


@router.get("/auth/logout")
async def logout(cookie_storage: EncryptedCookieStorage = EncryptedCookieStorage):
    r"""
    logout the current user
    """
    del cookie_storage[CookieKey.SESSION_ID]
    return cookie_storage.to_redirect_response("/")
