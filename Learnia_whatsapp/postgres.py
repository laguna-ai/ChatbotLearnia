import time
import json
from RAG.SysPrompt import sysPrompt
import os
import psycopg2


def create_postgres_connection():
    # open database connection
    PASSWORD = os.environ["POSTGRES_PASS"]
    DATABASE = "citus"
    USER = "citus"
    HOST = "c-learnia-postgres.mzd54eshacvnl4.postgres.cosmos.azure.com"
    PORT = "5432"

    connection = psycopg2.connect(
        database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    return connection


def find_or_create_session(conn, tel):
    with conn.cursor() as cur:
        # Consulta unificada usando CTEs para manejar la lógica de usuario y sesión
        query = """
        INSERT INTO sessions (id, history)
        SELECT 
            %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM sessions WHERE id = %s
        )
        ON CONFLICT (id) DO NOTHING
        RETURNING *;
        """

        params = (
            tel,
            json.dumps(sysPrompt),
            tel,
        )

        cur.execute(query, params)
        session = cur.fetchone()

        # Determinar si se dio la bienvenida basado en si se creó una sesión o no
        welcome = session is not None
        if not welcome:
            query1 = """
            SELECT * FROM sessions
            WHERE id = %s
            """
            cur.execute(query1, (tel,))
            session = cur.fetchone()

        conn.commit()

        return session[1], welcome # 1 for history


def update_session(conn, session_id, new_messages):

    new_messages_json = json.dumps(new_messages)

    with conn.cursor() as cur:
        # Concatena el arreglo JSONB existente con el nuevo arreglo de mensajes
        query = """
        UPDATE sessions
        SET history = history || %s::jsonb
        WHERE id = %s
        """

        cur.execute(query, (new_messages_json, session_id))
        conn.commit()


















