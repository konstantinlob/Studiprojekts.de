#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import fastapi
import sqlalchemy as sql
import sqlalchemy.orm
from database import createLocalSession, models as dbm
from gitalytics_api.cookies import active_workspace_id


router = fastapi.APIRouter()


@fastapi.Depends
def get_database_connection():
    db = createLocalSession()
    try:
        yield db
    finally:
        db.close()


@fastapi.Depends
def get_commit_count_subquery(
        connection: sql.orm.Session = get_database_connection,
        workspace_id: int = active_workspace_id,
        year: int = fastapi.Query()
):
    repos = connection.query(dbm.Repository.id).filter(dbm.Repository.workspace_id == workspace_id)
    commits = connection.query(dbm.Commit.id).filter(dbm.Commit.repository_id.in_(repos))
    return connection \
        .query(sql.func.count().label("count"),
               dbm.Commit.committed_at.label("date")) \
        .filter(dbm.Commit.id.in_(commits),
                sql.func.extract("year", dbm.Commit.committed_at) == year) \
        .group_by(sql.func.extract("month", dbm.Commit.committed_at),
                  sql.func.extract("day", dbm.Commit.committed_at)) \
        .subquery()


@router.get("/commits-per-hour")
async def get_commits_per_hour(
        connection: sql.orm.Session = get_database_connection,
        subquery=get_commit_count_subquery
):
    stats = connection \
        .query(sql.func.sum(subquery.c.count).label("count"),
               sql.func.extract("hour", subquery.c.date).label("hour")) \
        .group_by(sql.func.extract("hour", subquery.c.date)) \
        .all()

    return {row.hour: row.count for row in stats}


@router.get("/commits-per-weekday")
async def get_commits_per_weekday(
        connection: sql.orm.Session = get_database_connection,
        subquery=get_commit_count_subquery
):
    r"""
    please note:
        weekday of 0 means sunday
    """
    # 'dow' == day-of-week
    stats = connection \
        .query(sql.func.sum(subquery.c.count).label("count"),
               sql.func.extract("dow", subquery.c.date).label("weekday")) \
        .group_by(sql.func.extract("dow", subquery.c.date)) \
        .all()

    # could add to convert 0=sunday to 0=monday (wd - 1) % 7
    # but not because of https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getDay
    return {row.weekday: row.count for row in stats}


@router.get("/commits-per-day-in-month")
async def get_commits_per_day_in_month(
        connection: sql.orm.Session = get_database_connection,
        subquery=get_commit_count_subquery
):
    stats = connection \
        .query(sql.func.sum(subquery.c.count).label("count"),
               sql.func.extract("day", subquery.c.date).label("day")) \
        .group_by(sql.func.extract("day", subquery.c.date)) \
        .all()

    return {row.day: row.count for row in stats}


@router.get("/commits-per-week")
async def get_commits_per_week(
        connection: sql.orm.Session = get_database_connection,
        subquery=get_commit_count_subquery
):
    stats = connection \
        .query(sql.func.sum(subquery.c.count).label("count"),
               sql.func.extract("week", subquery.c.date).label("week")) \
        .group_by(sql.func.extract("week", subquery.c.date)) \
        .all()

    return {row.week: row.count for row in stats}


@router.get("/commits-per-month")
async def get_commits_per_month(
        connection: sql.orm.Session = get_database_connection,
        subquery=get_commit_count_subquery
):
    stats = connection \
        .query(sql.func.sum(subquery.c.count).label("count"),
               sql.func.extract("month", subquery.c.date).label("month")) \
        .group_by(sql.func.extract("month", subquery.c.date)) \
        .all()

    return {row.month: row.count for row in stats}
