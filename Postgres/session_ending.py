import datetime
import time

# funciones de time trigger


def get_sessions_to_finish(conn):

    # Calcula la fecha límite para las sesiones activas (18 horas antes de ahora)
    cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(hours=18)
    cutoff_timestamp = cutoff_time.timestamp()

    with conn.cursor() as cur:
        query = """
            SELECT * FROM sessions
            WHERE CAST(created_at AS BIGINT)< %s
        """
        cur.execute(query, (cutoff_timestamp,))
        sessions_to_update = cur.fetchall()

    return sessions_to_update


def finish_session(conn, session):
    ID = session[0]
    history = session[1]
    created_at = session[2]
    closed_at = time.time()

    with conn.cursor() as cur:
        query = """
        INSERT INTO closed_sessions (id, history, closed_at, created_at)
        SELECT %s, %s, %s, to_timestamp(%s)
        WHERE id = %s
        """
        cur.execute(query, (ID, history, closed_at, created_at))
        query_delete = """
        DELETE FROM mi_tabla WHERE id = %s;
        """
        cur.execute(query_delete, (ID,))
        conn.commit()