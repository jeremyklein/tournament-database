#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DATABASE = "dbname=tournament" # GLOBAL VARIABLE THAT IS NAME OF DATABASE


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection. Updated to handle missing DB"""
    try :
        return(psycopg2.connect(DATABASE))
    except:
        print "I am unable to connect to the database"

def deleteMatches():
    """Remove all the match records from the database."""
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""DELETE FROM Match""")
    conn.commit()

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
    cmd=("INSERT INTO Player(FullName) VALUES(%s);")
    cursor.execute(cmd,(name,))# inserts name into player table
    connection.commit()

def createRound():

    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""SELECT MAX(RoundNum) FROM Round """)
    roundNum=cursor.fetchall()[0][0]
    if (roundNum==None):
        roundNum=1
    else:
        roundNum=roundNum+1
    cursor.execute("""INSERT INTO Round(RoundNum=%s) VALUES(%s); """,(roundNum,))
    cursor.execute("""SELECT MAX(RoundId) from Round""")
    roundid=cursor.fetchall()[0][0]
    
    conn.commit()

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

    standings=[]
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(""" SELECT p.PlayerId, p.fullname, a.wins, count(m.matchid)
        FROM
            Player p
            left join match m on p.PlayerId=m.PlayerId
            left join 
                    (SELECT
                        COUNT(o.outcome) as wins, m.PlayerId
                        FROM Match m 
                        JOIN Outcome o
                            on o.outcomeid=m.outcomeid
                    WHERE o.outcome='win'
                    GROUP BY m.PlayerId
                        ) a
            on a.PlayerId=p.PlayerId

        GROUP BY p.PlayerId, p.fullname, a.wins, m.matchid

        """)
    results=cursor.fetchall()
    for i in range(0, countPlayers()):
        standings.append((results[i][0],
            results[i][1],
            int((results[i][2]) or 0),
            int(results[i][3]),))
    print standings
    return standings    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT max(matchid) from match")
    maxid=(cursor.fetchall()[0][0] or 0)+1
    cmd=("INSERT INTO Match(Outcomeid,Matchid,Playerid) VALUES(%s,%s,%s)")
    cursor.execute("SELECT Outcomeid from Outcome where Outcome='win'")
    winid=cursor.fetchall()[0][0]
    cursor.execute("SELECT Outcomeid from Outcome where Outcome='loss'")
    lossid=cursor.fetchall()[0][0]
    cursor.execute(cmd,(winid,maxid,winner))
    cursor.execute(cmd,(lossid,maxid,loser))
    conn.commit()

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
    swissPairings=[]
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(""" SELECT p.PlayerId, p.fullname, sum(o.value)
        FROM
            Player p
            left join match m on p.PlayerId=m.PlayerId
            left join outcome o on o.outcomeid=m.outcomeid

        GROUP BY p.PlayerId, p.fullname
        ORDER BY sum(o.value) 
        """)
    results=cursor.fetchall()
    for i in range(0, countPlayers(),2):
        swissPairings.append((results[i][0],results[i][1],results[i+1][0],results[i+1][1],))
    return swissPairings    

def createMatch(PlayerOne,PlayerTwo, Round):
    """
    Used to create a match in the database between two players
    """
    conn=conenct()
    cursor=connn.cursor()
    cursor.execute("""
        INSERT into
        """)

def addPlayers(num_Players):
    for i in range(num_Players):
        name=raw_input("Enter Player name: ")
        registerPlayer(name)


