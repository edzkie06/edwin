import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'rct.db')


def get_conn():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute('PRAGMA foreign_keys = ON')

    return conn



def init_db():

    conn = get_conn()

    conn.executescript('''

    CREATE TABLE IF NOT EXISTS user (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    role TEXT DEFAULT 'STAFF',

    status TEXT DEFAULT 'ACTIVE',

    created_at TEXT,

    updated_at TEXT

);

CREATE TABLE IF NOT EXISTS audit_logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    username TEXT,

    action TEXT,

    target TEXT,

    details TEXT,

    ip_address TEXT,

    created_at TEXT

);


    CREATE TABLE IF NOT EXISTS site (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE NOT NULL

    );


    CREATE TABLE IF NOT EXISTS record (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        site_id INTEGER NOT NULL,

        processed_by TEXT,

        created_at TEXT,

        indication TEXT,

        fa_name TEXT,

        ip_address TEXT,

        game TEXT,

        username_field TEXT,

        account_name TEXT,

        account_number TEXT,

        FOREIGN KEY(site_id) REFERENCES site(id)
        ON DELETE CASCADE

    );


    CREATE TABLE IF NOT EXISTS kpi_data (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    AGENT TEXT,

    DEPOSIT TEXT,

    WITHDRAWAL TEXT,

    NET_DEPOSIT TEXT,

    PLAYER_COUNT TEXT,

    VTO TEXT,

    WINLOSS TEXT,

    COMMS TEXT,

    COMMS_PERCENT TEXT,

    OVER_ALL TEXT

);


    ''')


    conn.commit()

    conn.close()



def seed_defaults(generate_password_hash):

    conn = get_conn()


    # DEFAULT ADMIN

    user = conn.execute(
        'SELECT COUNT(*) AS c FROM user'
    ).fetchone()


    if user['c'] == 0:

        conn.execute(
    '''
    INSERT INTO user
    (username,password_hash,role,status,created_at,updated_at)
    VALUES (?,?,?,?,?,?)
    ''',
    (
        'admin',
        generate_password_hash('changeme123'),
        'ADMIN',
        'ACTIVE',
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
)


        print(
            "Created admin account: admin / changeme123"
        )



    # DEFAULT SITES

    default_sites = [

        "TMT",

        "MGK",

        "BUENAS"

    ]


    for site in default_sites:

        check = conn.execute(

            'SELECT 1 FROM site WHERE name=?',

            (site,)

        ).fetchone()



        if not check:

            conn.execute(

                'INSERT INTO site(name) VALUES(?)',

                (site,)

            )



    conn.commit()

    conn.close()