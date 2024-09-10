import azure.functions as func
from Postgres.postgres import (
    create_postgres_connection,
)
from Postgres.session_ending import (
    get_sessions_to_finish,
    finish_session,
)
from .insights import get_insights
from MSAL.search import add_to_list, site_ID, list_ID

def main(mytimer: func.TimerRequest) -> None:  # pylint: disable=unused-argument

    with create_postgres_connection() as conn:  # pylint: disable=E1129
        sessions_to_finish = get_sessions_to_finish(conn)

        for s in sessions_to_finish:
            analysis = get_insights(s)
            add_to_list(site_ID, list_ID, analysis)
            finish_session(conn, s)
