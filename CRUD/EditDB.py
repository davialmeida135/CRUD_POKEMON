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

def update_pokemon(conn, pokemon):
    """
    update priority, begin_date, and end date of a pokemon
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
    cur.execute(sql, pokemon)
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
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons")

    rows = cur.fetchall()
    return rows

def select_pokemon_by_name(conn, name):
    """
    Query pokemon by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons WHERE name=?", (str(name)))

    rows = cur.fetchall()

    return rows

def select_pokemon_by_id(conn, id):
    """
    Query pokemon by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pokemons WHERE img=?", (id))

    rows = cur.fetchall()

    return rows
    
def main():

    database = "db\pokemons.db"
    conn = create_connection(database)

    if conn is not None:
           # create projects table
        poke1 = (1,"Charmander","Fire","batata")
        poke2 = (2,"Slugma","Fire","batata")
        poke3 = (3,"Tepig","Fire","batata")
        poke4 = (4,"Squirtle","Water","batata")
        poke5 = (7,"Totodile","Water","batata")
        poke8 = Pokemon(8,"Pikachu","Electric","https://upload.wikimedia.org/wikipedia/en/thumb/a/a6/Pokémon_Pikachu_art.png/220px-Pokémon_Pikachu_art.png")
        ''' 
        delete_pokemon(conn,1)

        create_pokemon(conn,poke1)
        create_pokemon(conn,poke2)
        create_pokemon(conn,poke3)
        create_pokemon(conn,poke4)
        create_pokemon(conn,poke5)

        create_pokemon(conn,poke5)'''

        create_pokemon(conn,(poke8.id,poke8.name,poke8.type,poke8.img))
        a = select_all_pokemon(conn)
        print(len(a))
       



    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
