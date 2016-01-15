#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    return conn, cur


def disconnect(conn, cur):
    """Disconnect from the PostgreSQL database."""
    cur.close()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cur = connect()
    cur.execute("DELETE FROM matches;")
    conn.commit()
    disconnect(conn, cur)


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("DELETE FROM players;")
    conn.commit()
    disconnect(conn, cur)


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    cur.execute("SELECT count(*) FROM players;")
    ret = cur.fetchall()
    disconnect(conn, cur)
    return ret[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    cur.execute("INSERT INTO players VALUES (%s);", (name,))
    conn.commit()
    disconnect(conn, cur)


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
    conn, cur = connect()
    cur.execute("""
    SELECT players.id, players.name, wins.count as wins, count(matches.id) as matches
    FROM players
    LEFT JOIN matches
    ON players.id = matches.winner OR players.id = matches.loser
    LEFT JOIN wins
    ON players.id = wins.id
    GROUP BY players.id, players.name, wins.count
    ORDER BY wins.count DESC;
    """)                        # Please kindly comment me if it could be simpler.
    ret = cur.fetchall()
    disconnect(conn, cur)
    return ret


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cur = connect()
    cur.execute("INSERT INTO matches VALUES (%s, %s);", (winner, loser))
    conn.commit()
    disconnect(conn, cur)
 

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
    win_list = playerStandings()
    ret = []
    for i in range(len(win_list) / 2):
        ret.append((win_list[i*2][0], win_list[i*2][1], win_list[i*2+1][0], win_list[i*2+1][1]))
    return ret
