import psycopg2
from uuid import uuid4

def get_db_connection():
    return {
        'host': '127.0.0.1',
        'database': 'culturalheritage',
        'user': 'postgres',
        'password': 'password',
        'port': 5432
    }

def insert_site(name, year, platform, publisher): 
    connection = psycopg2.connect(**get_db_connection())
    cursor = connection.cursor()
    cursor.execute("""
                    INSERT INTO culturalheritage.site (game_id, publisher, platform, name, year)
                    VALUES (%s, %s, %s, %s, %s);
                """, (str(uuid4()), publisher, platform, name, year))
    connection.commit()

    cursor.close()
    connection.close()
    print(f"Successfully inserted {name} into the games table.")

def get_games():
    connection = psycopg2.connect(**get_db_connection())
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT * FROM game_store.game;
                """)
    print(cursor.fetchall())
    cursor.close()
    connection.close()

def update_publisher(game_name, newPublisherName):
    connection = psycopg2.connect(**get_db_connection())
    cursor = connection.cursor()
    cursor.execute("""
                    UPDATE game_store.game
                    SET publisher = %s
                    WHERE name = %s;
                """, (newPublisherName, game_name))
    connection.commit()

    cursor.close()
    connection.close()
    print(f"Successfully updated the publisher for {game_name} to {newPublisherName}.")

def delete_game(game_name):
    connection = psycopg2.connect(**get_db_connection())
    cursor = connection.cursor()
    cursor.execute("""
                    DELETE FROM game_store.game
                    WHERE name = %s;
                """, (game_name,))
    connection.commit()

    cursor.close()
    connection.close()
    print(f"Successfully deleted {game_name}.")