import flask
import tiamat as tiamat

from flask_cors import CORS

from flask_mysqldb import MySQL
import db_config
from tiamat_db_functions import *


# Create the Flask app
app = flask.Flask(__name__)

#initialize app database config settings
app.config['MYSQL_HOST'] = db_config.Config.HOST
app.config['MYSQL_USER'] = db_config.Config.USER
app.config['MYSQL_PASSWORD'] = db_config.Config.PASSWORD
app.config['MYSQL_DB'] = db_config.Config.DATABASE

mysql = MySQL(app)

CORS(app)

chat = tiamat.Tiamat()

# Prompts the Tiamat module with a message and optional code and history,
# and retrieves personalization instructions from the database if possible,
# then returns the chatbot's response
@app.route('/api/prompt', methods=['POST'])
def prompt_tiamat():
    # Extract necessary data from the request
    data = flask.request.get_json()
    user_id = data.get('id')
    message = data.get('message')
    code = data.get('code') or ''
    history = data.get('history') or []

    # Reject request if required data is missing
    if not message or not user_id:
        return flask.jsonify({'message': 'Some required data is missing'}), 400

    # Log the data
    print(f"User ID: {user_id}")
    print(f"User's message: {message}")
    print(f"Code:\n{code}")
    print(f"History:\n{history}")
    
    # TODO: Retrieve user's personalization instructions from the database
    personalization = ""
    
    # Get chatbot response and log it
    response = chat(
        message, 
        code=code, 
        history=history, 
        personalization=personalization
    )

    print(f"Tiamat Response: {response.answer}")

    # Return the response
    return flask.jsonify({'response': response.answer})

@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    #ensures database is created and tables are initialized
    try:
        init_database(mysql)
    except:
        return flask.jsonify({'message': 'Something went wrong with database initialization'}), 400

    # Extract the prompt from the request
    data = flask.request.get_json()
    conversation_id = data.get('id')
    message = data.get('message')
    code = data.get('code') or ''
    response = data.get('response')
    rating = data.get('rating')
    
    if not message or not conversation_id or not response or rating == None:
        return flask.jsonify({'message': 'Some required data is missing'}), 400

    print(f"Feedback received for conversation {conversation_id}")
    cursor = make_connection(mysql)
    print("Connected to the database")

    #checks if user exists in the database, if not, adds them
    if (check_if_user_exists(conversation_id, cursor) == False):
        add_user(conversation_id, cursor)
        print(f"User {conversation_id} added")
    
    #checks if the interaction already exists in the database, if so, modifies the rating, if not, adds the feedback
    if (check_if_interaction_exists(conversation_id, message, response, code, cursor)):
        modify_interaction_rating(message, response, code, rating, cursor)
    else:
        add_feedback(cursor, conversation_id, message, code, response, rating)

    return flask.jsonify({'rating': rating, 'message': message, 'response': response, 'code': code})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
