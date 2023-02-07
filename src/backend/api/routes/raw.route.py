#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import fastapi
import httpx
import pydantic
from api.common import SessionToken, BearerAuth


class RawRequestsSettings(pydantic.BaseSettings):
    GITHUB_API_URL = "https://api.github.com"

    class Config:
        env_file = ".env"


settings = RawRequestsSettings()
router = fastapi.APIRouter(prefix="/raw")


class MeResponseModel(pydantic.BaseModel):
    login: str
    avatar_url: str
    html_url: str
    type: t.Literal["User"]
    blog: t.Optional[str]


@router.get("/me", summary="Get current User", response_model=MeResponseModel,
            responses={
                fastapi.status.HTTP_401_UNAUTHORIZED: {}
            })
async def raw_me(token: str = SessionToken):
    async with httpx.AsyncClient(base_url=settings.GITHUB_API_URL) as client:
        response = await client.get("/user", auth=BearerAuth(token))
        if not response.is_success:
            raise fastapi.HTTPException(response.status_code, detail=response.reason_phrase)
        return response.json()
