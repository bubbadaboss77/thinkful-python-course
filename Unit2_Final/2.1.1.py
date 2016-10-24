import logging
import argparse
import psycopg2
import psycopg2.extras


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
    
        try:
            cursor.execute("insert into snippets values (%s, %s)",(name, snippet))
        except psycopg2.IntegrityError:
            connection.rollback()
            cursor.execute("update snippets set message=%s, hidden=%s where keyword=%s",(snippet, hide, name))
            connection.commit()
    
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    
    print(name)
    
    logging.info("Reading snippet {!r}".format(name))
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    
    if not row:
        # No snippet was found with that name.
        return "404: Snippet Not Found"
    
    return row[0]
    
def catalog():
    #querying the snippets db for all keys and their names
    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(
            "select keyword from snippets")
        rows = cursor.fetchall()
        for row in rows:
            print(row['keyword'])
    logging.debug("Query complete")
        

def main():
    
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    #subparser for the get command
    logging.debug("Constructing retrieve subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    #subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    subparsers.add_parser("catalog", help="Query snippet keywords")

    arguments = parser.parse_args()
    
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        catalog()
        print('retrieved keys:')
   
        
if __name__ == '__main__':
    main()