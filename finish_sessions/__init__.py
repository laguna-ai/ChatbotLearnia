import azure.functions as func
from Postgres.postgres import (
    create_postgres_connection,
)
from Postgres.session_ending import (
    get_sessions_to_finish,
    finish_session,
)
from .Sharepoint import add_to_Sharepoint_list
from .insights import get_insights


def main(mytimer: func.TimerRequest) -> None:  # pylint: disable=unused-argument

    with create_postgres_connection() as conn:
        sessions_to_finish = get_sessions_to_finish(conn)

        for s in sessions_to_finish:
            analysis = get_insights(s)
            add_to_Sharepoint_list(analysis)
            finish_session(conn, s)
