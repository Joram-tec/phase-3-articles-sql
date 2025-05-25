from Lib.db.connection import get_connection

def data_base():
    conn = get_connection()
    cursor = conn.cursor()

    with open ("Lib/db/schema.sql", "r") as file:
        conn.executescript(file.read())
    conn.commit()
    conn.close()    

if __name__ == "__main__":
    data_base()
    print("Database set-up done!")