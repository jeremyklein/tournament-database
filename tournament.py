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
    conn=connect() # creates connection
    cursor=conn.cursor() # creates cursor
    cursor.execute("""DELETE FROM Match""") # deletes all records from match
    conn.commit() # commits changes

def deletePlayers():
    """Remove all the player records from the database."""
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cursor.execute("DELETE FROM Player;")# inserts name into player table
    connection.commit() # commits changes

def countPlayers():
    """Returns the number of players currently registered."""
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cursor.execute("select count(fullname) from player;")# inserts name into player table
    return(cursor.fetchall()[0][0]) # returns the value of the only row in the query

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection=connect() # calls the connect method which returns a db connection
    cursor=connection.cursor()# calls the cursor method from pscopg2
    cmd=("INSERT INTO Player(FullName) VALUES(%s);")#query string
    cursor.execute(cmd,(name,))# inserts name into player table using parameterized query
    connection.commit() # commits changes


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

    standings=[]# empty array for standing
    conn=connect()# creates connectin
    cursor=conn.cursor() #creates cursor
    cursor.execute(""" SELECT p.PlayerId, p.fullname, a.wins, count(m.matchid) -- returns player, name, wins, and match count
        FROM
            Player p --player table containts playerid and player name
            left join match m on p.PlayerId=m.PlayerId -- match table is related to player table with player id
            left join 
                    (SELECT -- this query returns the number of wins a player has
                        COUNT(o.outcome) as wins, m.PlayerId
                        FROM Match m 
                        JOIN Outcome o
                            on o.outcomeid=m.outcomeid
                    WHERE o.outcome='win'
                    GROUP BY m.PlayerId
                        ) a
            on a.PlayerId=p.PlayerId

        GROUP BY p.PlayerId, p.fullname, a.wins, m.matchid -- because the select statement includes an aggregation (count) values must be grouped

        """)
    results=cursor.fetchall() # results are stored
    for i in range(0, countPlayers()): # for all players
        standings.append((results[i][0], # add tuple to array
            results[i][1],
            int((results[i][2]) or 0), 
            int(results[i][3]),))
    return standings    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn=connect()# create connection
    cursor=conn.cursor() # create cursor
    cursor.execute("SELECT max(matchid) from match") # Get the latest match number
    maxid=(cursor.fetchall()[0][0] or 0)+1 # create a new match id
    cmd=("INSERT INTO Match(Outcomeid,Matchid,Playerid) VALUES(%s,%s,%s)") # string template to insert new values
    cursor.execute("SELECT Outcomeid from Outcome where Outcome='win'") #get the id for outcome
    winid=cursor.fetchall()[0][0] # return only value of this query
    cursor.execute("SELECT Outcomeid from Outcome where Outcome='loss'") # get the id for outcome
    lossid=cursor.fetchall()[0][0] #return only value of this query
    cursor.execute(cmd,(winid,maxid,winner)) # insert values into database for winner
    cursor.execute(cmd,(lossid,maxid,loser)) # insert values into database for loser
    conn.commit()# commit connection to save values

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
    swissPairings=[] # create empty array
    conn=connect()# create connection to database
    cursor=conn.cursor() # cursor for connection
    cursor.execute(""" SELECT p.PlayerId, p.fullname, sum(o.value) -- return payer id full name and the sum of outcome
        FROM
            Player p
            left join match m on p.PlayerId=m.PlayerId
            left join outcome o on o.outcomeid=m.outcomeid

        GROUP BY p.PlayerId, p.fullname
        ORDER BY sum(o.value) 
        """)
    results=cursor.fetchall() # save results
    for i in range(0, countPlayers(),2): # iterate through the results
        swissPairings.append((results[i][0],results[i][1],results[i+1][0],results[i+1][1],)) # pair the players in order of the list
    return swissPairings    


def addPlayers(num_Players):
    """Helper method for personal testing to add an arbitrary number of new players to the database
    """
    for i in range(num_Players):
        name=raw_input("Enter Player name: ")
        registerPlayer(name)


