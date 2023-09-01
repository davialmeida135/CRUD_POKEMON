import sqlite3
from sqlite3 import Error
from dataclasses import dataclass

@dataclass
class Pokemon:
    id: int
    name: str
    type: str
    img: str

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

def update_pokemon(conn, id, name, type, img):
    """
    update id, name, type, img of a pokemon
    :param conn:
    :param pokemon:
    :return: project id
    """
    sql ='''UPDATE pokemons
            SET name = ? ,
                type = ? ,
                img = ?
            WHERE id = ?
        '''
    cur = conn.cursor()
    cur.execute(sql,(name,type,img,id))
    conn.commit()

def delete_pokemon(conn, id):
    """
    Delete a pokemon by pokemon id
    :param conn:  Connection to the SQLite database
    :param id: id of the pokemon
    :return:
    """
    sql = 'DELETE FROM pokemons WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all_pokemon(conn):
    """
    Query all rows in the pokemons table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons")

    rows = cur.fetchall()
    return rows

def select_pokemon_by_name(conn, name):
    """
    Query pokemon by name
    :param conn: the Connection object
    :param name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons WHERE name=?", (str(name),))

    rows = cur.fetchall()

    return rows

def select_pokemon_by_id(conn, id):
    """
    Query pokemon by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons WHERE id=?", (id,))

    rows = cur.fetchall()

    return rows
    
def main():

    database = "db\pokemons.db"
    conn = create_connection(database)
    '''
    if conn is not None:
        # create projects table
         poke1 = (1,"Charmander","Fire","batata")


    else:
        print("Error! cannot create the database connection.")
    '''

if __name__ == '__main__':
    main()
