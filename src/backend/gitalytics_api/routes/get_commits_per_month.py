import fastapi
import sqlalchemy as sql
from database import models as dbm, DatabaseSession
from gitalytics_api import active_workspace_id, get_database_connection, session_from_cookies


router = fastapi.APIRouter()

@router.get("/commits-per-month")
async def get_commits_per_month(
        connection: DatabaseSession = get_database_connection,
        session: dbm.Session = session_from_cookies,
        workspace_id: int = active_workspace_id,
        year: int = fastapi.Query(gt=0),
):
    stats = connection \
        .query(sql.func.extract("month", dbm.Commit.committed_at).label("month"),
               sql.func.count().label("count")) \
        .select_from(dbm.Session) \
        .join(dbm.Repository, dbm.Session.repositories) \
        .join(dbm.Commit, dbm.Repository.commits) \
        .filter(dbm.Session.id == session.id) \
        .filter(dbm.Repository.workspace_id == workspace_id) \
        .filter(sql.func.extract("year", dbm.Commit.committed_at) == year) \
        .group_by(sql.func.extract("month", dbm.Commit.committed_at)) \
        .all()

    return {row.month: row.count for row in stats}