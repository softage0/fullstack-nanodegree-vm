#
# Database access functions for the web forum.
# 

import time
import psycopg2


def GetAllPosts():
    """Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    """
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()
    cur.execute("delete from posts where content like '%spam%';")
    conn.commit()
    cur.execute("select * from posts order by time desc;")
    db = cur.fetchall()
    cur.close()
    conn.close()
    posts = [{'content': str(row[0]), 'time': time.strftime('%c', row[1].timetuple())} for row in db]
    return posts


def AddPost(content):
    """Add a new post to the database.

    Args:
      content: The text content of the new post.
    """
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()
    cur.execute("INSERT INTO posts VALUES (%s)", (content,))
    conn.commit()
    cur.close()
    conn.close()
