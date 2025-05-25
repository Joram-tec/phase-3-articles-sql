from lib.db.connection import get_connection

def data_base():
    conn = get_connection()
    with open ("lib/db/schema.sql") as file:
        conn.executescript(file.read())
    conn.commit()
    conn.close()    

if __name__ == "__main__":
    data_base()
    print("Database set-up done!")