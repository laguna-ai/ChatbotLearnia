from Postgres.postgres import (
    create_postgres_connection,
)
from Postgres.session_ending import (
    get_sessions_to_finish,
    finish_session,
)
from finish_sessions.Sharepoint import add_to_Sharepoint_list
from finish_sessions.insights import get_insights


def main():  

    with create_postgres_connection() as conn:
        sessions_to_finish = get_sessions_to_finish(conn)
        
        for s in sessions_to_finish:
            analysis = get_insights(s)
            add_to_Sharepoint_list(analysis)
            finish_session(conn, s)

main()            