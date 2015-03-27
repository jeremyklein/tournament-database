#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection. Updated to handle missing DB"""
    try :
        return(psycopg2.connect("dbname=tournament"))
    except:
        print "I am unable to connect to the database"


def deleteMatches():
    """Remove all the match records from the database."""


def deletePlayers():
    """Remove all the player records from the database."""
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cursor.execute("DELETE FROM Player;")# inserts name into player table
    connection.commit()

def countPlayers():
    """Returns the number of players currently registered."""
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cursor.execute("select count(fullname) from player;")# inserts name into player table
    return(cursor.fetchall()[0][0])



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cursor.execute("insert into Player(fullname) values('%s');"%(name,))# inserts name into player table
    connection.commit()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""SELECT p.PlayerId, p.fullname, sum(o.value)
        FROM
            Player p
            join playermatch m on p.PlayerId=m.PlayerId
            join outcome o on o.outcomeid=m.outcomeid

        GROUP BY p.PlayerId, p.fullname
                """    )
    if(cursor.fetchall()==[]):
        simFirstRound()
    else:
        print("Houston we have a bigger problem")

def simFirstRound():
    numPlayers=countPlayers()
    conn=connect()
    cursor=conn.cursor()
    players=cursor.execute("""
        SELECT PlayerId from Player;
    """)
    cursor.execute("""INSERT INTO Round(RoundName) Values(1)""")
    conn.commit()
    for i in range(0,numPlayers,2):
        cursor.execute("""INSERT INTO match
            """)

def addPlayers(num_Players):
    for i in range(num_Players):
        name=raw_input("Enter Player name: ")
        registerPlayer(name)

def main():
    simFirstRound()

main()