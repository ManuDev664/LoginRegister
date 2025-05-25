import psycopg2

def get_connection():
    return psycopg2.connect(
        host="192.160.51.150",
        database="ErciUsers",
        user="postgres",
        password="50_dam50",
        port="5432"
    )

def create_users_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id serial primary key,
                    nombre varchar(50) not null,
                    apellidos varchar(50) not null,
                    email varchar(100) unique not null,
                    username varchar(50) not null,
                    password varchar(50) not null,
                    fechaNacimiento date not null,
                    estado boolean default true,
                    fechaRegistro timestamp default current_timestamp,
                    rol varchar(5) default 'user',
                    ultimo_login timestamp
                );
            """)
            conn.commit()

def get_user(username_or_email, password):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s
            """, (username_or_email, username_or_email, password))
            return cur.fetchone()

def update_last_login(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET ultimo_login = NOW() WHERE id = %s", (user_id,))
            conn.commit()

def insert_user(nombre, apellidos, username, email, password, fechaNacimiento):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (nombre, apellidos, username, email, password, fechaNacimiento)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellidos, username, email, password, fechaNacimiento))
            conn.commit()

def user_exists(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            return cur.fetchone() is not None


def eliminar_usuario(user_id):
    if not user_exists(user_id):
        return False
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error en delete_user: {e}")
        return False
    finally:
        conn.close()

def check_user(username_or_email, password):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s
            """, (username_or_email, username_or_email, password))
            user = cur.fetchone()
            return user
