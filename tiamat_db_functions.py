
#RUN THIS FIRST TO CREATE THE DATABASE
def init_database(sqlObj):
    cursor = sqlObj.connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS tiamat_db")
    cursor.execute("USE tiamat_db")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (userID INT PRIMARY KEY, personalizedPrompt TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS interactions (userID INT, userMessage TEXT, code TEXT, tiamatResponse TEXT, rating INT, FOREIGN KEY (userID) REFERENCES users(userID))")
    cursor.connection.commit()

    print("Tables created")

    return cursor

def make_connection(sqlObj):
    
    cursor = sqlObj.connection.cursor()

    return cursor

def add_feedback(cursor, conversation_id, message, code, response, rating):
    cursor.execute("INSERT INTO interactions (userID, userMessage, code, tiamatResponse, rating) VALUES (%s, %s, %s, %s, %s)", (conversation_id, message, code, response, rating))
    cursor.connection.commit()

    print("Feedback added")

    return cursor

def add_user(userID, cursor):
    cursor.execute("INSERT INTO users (userID) VALUES (%s)", (userID,))
    cursor.connection.commit()

    print("User added")

    return cursor

def check_if_user_exists(userID, cursor):
    cursor.execute("SELECT * FROM users WHERE userID = %s", (userID,))
    result = cursor.fetchall()

    if len(result) == 0:
        return False
    else:
        return True

def check_if_interaction_exists(userID, message, response, code, cursor):
    cursor.execute("SELECT * FROM interactions WHERE userMessage = %s AND tiamatResponse = %s AND code = %s AND userID = %s", (message, response, code, userID))
    result = cursor.fetchall()

    if len(result) == 0:
        return False
    else:
        return True
    
def modify_interaction_rating(message, response, code, rating, cursor):
    cursor.execute("UPDATE interactions SET rating = %s WHERE userMessage = %s AND tiamatResponse = %s AND code = %s", (rating, message, response, code))
    cursor.connection.commit()

    print("Rating modified")

    return cursor