import psycopg2
from config import config_setup
from config import config_live
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def createDB():
    """
    Creates the database using the configuration from config_setup.ini
    """
    conn=None
    try:
        params=config_setup()
        conn= psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur=conn.cursor()
        cur.execute("CREATE DATABASE FIRST")
        cur.close()

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()


def createTables():
    """
    creates the appropriate tables in the database
    """
    conn=None
    try:
        params=config_live()
        conn=psycopg2.connect(**params)
        cur=conn.cursor()
        cur.execute("create table storage (storage_id BIGSERIAL PRIMARY KEY, service varchar(256), username varchar(256), password varchar(256))")
        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    createDB()
    createTables()







