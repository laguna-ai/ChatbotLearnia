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
import logging

def main(mytimer: func.TimerRequest) -> None:  # pylint: disable=unused-argument
    logging.info("Python timer trigger function started")
    with create_postgres_connection() as conn:  # pylint: disable=E1129
        logging.info("Connected to Postgres")
        # Get the sessions that need to be finished 
        sessions_to_finish = get_sessions_to_finish(conn)
        logging.info(f"Sessions to finish: {len(sessions_to_finish)}")
        for s in sessions_to_finish:
            analysis = get_insights(s)
            logging.info(f"Analysis of session {s[0]}: {analysis}")
            add_to_Sharepoint_list(analysis)
            logging.info(f"Analysis Added to Sharepoint")
            finish_session(conn, s)
            logging.info(f"Session {s[0]} finished")
