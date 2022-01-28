import praw
from prawcore import OAuthException
from dotenv import load_dotenv, dotenv_values
import sqlite3
import csv


def get_user_info(_id: str, secret: str, agent: str, 
                  user: str, _pass: str, _2fa: str) -> praw.Reddit:
    """Get access to a Reddit account"""
    reddit_user = praw.Reddit(client_id=_id,
                              client_secret=secret,
                              user_agent=agent,
                              username=user,
                              password=_pass + _2fa)

    # Check that the credentials are valid.
    try:
        print("User:", reddit_user.user.me())
    except OAuthException as e:
        raise Exception(e, "TL;DR: Invalid credential(s)")
    return reddit_user


def access_database(name: str) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """Access the database containing saved content"""
    
    con = sqlite3.connect(name)
    cur = con.cursor()

    # Check if table exists, if not create it.
    # Note: If type = 0, it is a post.
    # Note: If typ6e = 1, it is a comment
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "saved" (
                    Sub TEXT NOT NULL,
                    Type  TEXT NOT NULL,
                    ID    TEXT NOT NULL,
                    Title    TEXT NOT NULL,
                    URL   TEXT NOT NULL,
                    PRIMARY KEY("ID")
                );''')
    return cur, con


def export_database(name_database: str, name_export: str = "exported.csv") -> None:
    """Export the database table 'saved' to csv"""
    
    database = access_database(name_database)
    cur = database[0]
    con = database[1]

    headers = cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('saved')")
    header_names = [i[0] for i in headers]

    with open(name_export, mode="w", encoding='utf-16') as f:
        # utf-16 is used to support more characters since Reddit
        # allows for a variety of characters for titles
        writer = csv.writer(f, lineterminator="\n", delimiter="\t")
        # Delimiter changed to tabs so that Excel can properly
        # display the columns
        writer.writerow(header_names)
        writer.writerows(cur.execute("SELECT * FROM saved"))
    con.close()


def main(name: str, use_file: bool = True) -> None:
    """The main program.

    :param name: The name of the database to view
    :param use_file: Whether or not to use a .env file for details
    """
    # Load credentials from .env file
    load_dotenv()
    config = dotenv_values(".env")

    # Access database and variables
    database = access_database(name)
    cur = database[0]
    con = database[1]

    # Access Reddit account
    if use_file:
        _2FA = ":" + input("2FA (if none, press enter): ")
        breakpoint()
        reddit = get_user_info(config["CLIENT_ID"], config["CLIENT_SECRET"],
                               config["USER_AGENT"], config["USER_NAME"],
                               config["USER_PASS"], _2FA)
        breakpoint()
    else:
        _client_id = input("CLIENT_ID: ")
        _client_secret = input("CLIENT_SECRET: ")
        _user_agent = input("USER_AGENT: ")
        _user_name = input("USER_NAME: ")
        _user_pass = input("USER_PASS: ")
        _2FA = input("2FA (if applicable, if not leave blank and press enter): ")

        reddit = get_user_info(_client_id, _client_secret, _user_agent,
                               _user_name, _user_pass, _2FA)
    # Record the saved posts and comments
    _note = ""
    for index, item in enumerate(reddit.user.me().saved(limit=None)):
        if isinstance(item, praw.reddit.models.Submission):
            content = {"sub": item.subreddit.display_name,
                       "type": 0,
                       "id": item.id,
                       "title": item.title,
                       "url": item.permalink}

        elif isinstance(item, praw.reddit.models.Comment):
            content = {"sub": item.subreddit.display_name,
                       "type": 1,
                       "id": item.id,
                       "title": item.submission.title,
                       "url": item.permalink}
        else:
            raise Exception("What was retrieved is neither a post nor comment. Suspicious.")

        try:
            # TODO: Use named style in the future
            cur.execute('''INSERT INTO saved VALUES
                        (?, ?, ?, ?, ?)''',
                        list(content.values()))
            con.commit()
            _note = "Success"
        except sqlite3.IntegrityError:
            _note = "Already in database"
        
        print(index, f"id: {content['id']}", f"type: {content['type']}", _note, sep=" - ")
    con.close()


if __name__ == "__main__":
    database_name = "information.db"
    main(database_name)
    export_database(database_name)
