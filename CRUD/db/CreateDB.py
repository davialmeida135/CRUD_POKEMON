import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_pokemon(conn, pokemon):
    """
    Create a new pokemon
    :param conn:
    :param pokemon:
    :return:
    """

    sql = ''' INSERT INTO pokemons(id,name,type,img)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pokemon)
    conn.commit()

def main():
    database = r"D:\Davi\FlaskTestes\CRUD\db\pokemons.db"

    
   
    texto = """CREATE TABLE pokemons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            img TEXT
            ); """
    
    conn = create_connection(database)

    if conn is not None:
        # create projects table
        #create_table(conn, texto)
        newpokemon = (1,"pikachu","electric","coolurl")
        create_pokemon(conn,newpokemon)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
