from flask import current_app

#RUN THIS FIRST TO CREATE THE DATABASE
def init_database(sqlObj):
    cursor = None

    try:
        cursor = sqlObj.connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS tiamat_db")
        cursor.execute("USE tiamat_db")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (uid INT AUTO_INCREMENT PRIMARY KEY, userID INT UNIQUE, personalizedPrompt TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS interactions (uid INT AUTO_INCREMENT PRIMARY KEY, userID INT, userMessage TEXT, code TEXT, tiamatResponse TEXT, rating INT, reason TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (userID) REFERENCES users(userID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS personas (uid INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, prompt TEXT)")
        cursor.connection.commit()

        cursor.close()
    except Exception as e:
        current_app.logger.error("Error initializing database", exc_info=True)
        raise
    finally:
        if cursor:
            cursor.close()

def make_connection(sqlObj):
    cursor = sqlObj.connection.cursor()
    return cursor

def add_feedback(cursor, conversation_id, message, code, response, rating, reason):
    cursor.execute("INSERT INTO interactions (userID, userMessage, code, tiamatResponse, rating, reason) VALUES (%s, %s, %s, %s, %s, %s)", (conversation_id, message, code, response, rating, reason))
    cursor.connection.commit()
    return cursor

def add_user(userID, cursor):
    cursor.execute("INSERT INTO users (userID) VALUES (%s)", (userID,))
    cursor.connection.commit()
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
    
def modify_interaction_rating(message, response, code, rating, reason, cursor):
    cursor.execute("UPDATE interactions SET rating = %s, reason = %s WHERE userMessage = %s AND tiamatResponse = %s AND code = %s", (rating, reason, message, response, code))
    cursor.connection.commit()

    return cursor

def get_users_interactions(userID, cursor, k=5):
    cursor.execute("SELECT * FROM interactions WHERE userID = %s ORDER BY created_at DESC LIMIT %s", (userID, k))
    result = cursor.fetchall()
    
    return result

def get_personalization(userID, cursor):
    cursor.execute("SELECT personalizedPrompt FROM users WHERE userID = %s", (userID,))
    result = cursor.fetchall()

    if len(result) == 0:
        return None
    
    return result[0][0]

def update_personalization(userID, prompt, cursor):
    cursor.execute("UPDATE users SET personalizedPrompt = %s WHERE userID = %s", (prompt, userID))
    cursor.connection.commit()

    return cursor

def add_persona(name, description, prompt, cursor):
    cursor.execute("INSERT INTO personas (name, description, prompt) VALUES (%s, %s, %s)", (name, description, prompt))
    cursor.connection.commit()

    return cursor

def update_persona(id, name, description, prompt, cursor):
    cursor.execute("UPDATE personas SET name = %s, description = %s, prompt = %s WHERE uid = %s", (name, description, prompt, id))
    cursor.connection.commit()

    return cursor

def delete_persona(id, cursor):
    cursor.execute("DELETE FROM personas WHERE uid = %s", (id,))
    cursor.connection.commit()

    return cursor

def get_personas(cursor):
    cursor.execute("SELECT * FROM personas")
    result = cursor.fetchall()

    return result

def get_persona(id, cursor):
    cursor.execute("SELECT * FROM personas WHERE uid = %s", (id,))
    result = cursor.fetchall()

    if len(result) == 0:
        return None
    
    return result[0]