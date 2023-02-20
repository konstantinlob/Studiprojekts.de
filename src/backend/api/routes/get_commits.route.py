#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import json
import typing
import fastapi
import pydantic
from api.database.models import Repository, Commit, Workspace
from api.database.db import createLocalSession
from sqlalchemy import select
from datetime import datetime

router = fastapi.APIRouter()

class CommitViewModel(pydantic.BaseModel):
    committed_at: datetime
    lines_removed: int
    author_id: int
    created_at: datetime
    lines_added: int
    files_modified: int
    repository_id: int
    id: int

    class Config:
        orm_mode = True

class ResponseModel(pydantic.BaseModel):
    commits: list[CommitViewModel]

@router.get("/commits", response_model=ResponseModel)
async def get_commits():
    r"""
    list all commits in the workspace
    """
    with createLocalSession() as session:
        statement = select(Commit, Repository).join(Repository.commits).filter(Repository.workspace_id == 1)
        commits = session.scalars(statement).all()

    return {"commits": commits}