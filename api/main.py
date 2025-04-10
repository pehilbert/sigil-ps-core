import flask
import llm.tiamat as tiamat
from llm.personas import Persona

from flask_cors import CORS

from flask_mysqldb import MySQL
import api.db_config as db_config
from api.tiamat_db_functions import *

# Disable caching globally to avoid __annotations__ bug
import litellm
litellm.cache = None

# Constants
MAX_FEEDBACK_ENTRIES = 5

# Create the Flask app
app = flask.Flask(__name__)

#initialize app database config settings
app.config['MYSQL_HOST'] = db_config.Config.HOST
app.config['MYSQL_USER'] = db_config.Config.USER
app.config['MYSQL_PASSWORD'] = db_config.Config.PASSWORD
app.config['MYSQL_DB'] = db_config.Config.DATABASE
app.config['MYSQL_CHARSET'] = db_config.Config.CHARSET
app.config['MYSQL_USE_UNICODE'] = db_config.Config.UNICODE

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
    personalize = data.get('personalize') or False
    persona_name = data.get('persona') or None

    # Reject request if required data is missing
    if not message or not user_id:
        return flask.jsonify({'message': 'Some required data is missing'}), 400

    # Log the data
    print(f"User ID: {user_id}")
    print(f"User's message: {message}")
    print(f"Code:\n{code}")
    print(f"History:\n{history}")
    print(f"Personalize: {personalize}")
    print(f"Persona name: {persona_name}")
    
    # Retrieve user's personalization instructions from the database if indicated
    cursor = make_connection(mysql)

    personalization = ""

    if personalize:
        print("Caller indicated that they want personalization.")

        personalization = get_personalization(user_id, cursor) or ""

        print(f"Personalized prompt retrieved: {personalization}")
    
    # Retrieve persona from the database if provided, otherwise default to Tiamat
    persona = Persona()

    if persona_name:
        print(f"Persona name provided: {persona_name}, retrieving from database...")
        persona_from_db = get_persona(persona_name, cursor)

        if not persona:
            return flask.jsonify({'message': 'Persona not found'}), 404

        persona = Persona(
            name=persona_from_db[1],
            description=persona_from_db[2],
            prompt=persona_from_db[3]
        )

    print(f"Persona to use: {persona}")

    cursor.close()

    # Get chatbot response and log it
    response = chat(
        message, 
        code=code, 
        history=history, 
        personalization=personalization,
        persona=persona
    )

    print(f"Tiamat Response: {response.answer}")

    # Return the response
    return flask.jsonify({'response': response.answer})

@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    print("Feedback received")

    # Extract the prompt from the request
    data = flask.request.get_json()
    user_id = data.get('id')
    message = data.get('message')
    code = data.get('code') or ''
    response = data.get('response')
    rating = data.get('rating')
    reason = data.get('reason')
    personalize = data.get('personalize') or False
    
    if not message or not user_id or not response or rating == None or not reason:
        return flask.jsonify({'message': 'Some required data is missing'}), 400

    print(f"Feedback received from user {user_id} for response: {response} (rating: {rating}, reason: {reason})")
    cursor = make_connection(mysql)
    print("Connected to the database")

    #checks if user exists in the database, if not, adds them
    if (check_if_user_exists(user_id, cursor) == False):
        add_user(user_id, cursor)
        print(f"User {user_id} added")
    
    #checks if the interaction already exists in the database, if so, modifies the rating, if not, adds the feedback
    if (check_if_interaction_exists(user_id, message, response, code, cursor)):
        modify_interaction_rating(message, response, code, rating, reason, cursor)
    else:
        add_feedback(cursor, user_id, message, code, response, rating, reason)

    # If the caller asked for personalization, update personalization for the user
    if personalize:
        print("Personalizing based on feedback...")

        # Get the user's interactions from the database
        interactions = get_users_interactions(user_id, cursor, k=MAX_FEEDBACK_ENTRIES)
        print("Interactions fetched from the database:", interactions)
        interactions = [f"Message: {interaction[2]}\nCode: {interaction[3]}\nResponse: {interaction[4]}\nRating: {interaction[5]}\nReason: {interaction[6]}" for interaction in interactions]
        print("Formatted interactions to get personalization instructions:", interactions)

        # Get existing personalized prompt from the database
        existing_personalization = get_personalization(user_id, cursor) or ""
        print("Existing personalization fetched from database:", interactions)

        # Use the interactions to get personalization instructions
        result = chat.get_personalization_from_feedback(interactions, existing_personalization)
        new_personalization = result.personalization
        reasoning = result.reasoning
        print("Tiamat reasoned about feedback:", reasoning)

        # Update personalization instructions in the database
        update_personalization(user_id, new_personalization, cursor)
        print("Updated personalization instructions:", new_personalization)

    cursor.close()

    return flask.jsonify({'rating': rating, 'reason': reason, 'message': message, 'response': response, 'code': code})

@app.route('/api/personalization/<int:user_id>', methods=['GET'])
def personalization_get(user_id):
    print("Request to get personalization for", user_id)

    cursor = make_connection(mysql)

    try:
        result = get_personalization(user_id, cursor)
    except Exception as e:
        cursor.close()
        
        print("Error retrieving personalization:", e)
        return flask.jsonify({'message': 'Something went wrong'}), 500
    
    print("Personalization retrieved:", result)

    cursor.close()

    if result == None:
        return flask.jsonify({'message': 'User not found'}), 404
    
    return flask.jsonify({'personalization': {"personalizedPrompt": result}})

@app.route('/api/personalization/<int:user_id>', methods=['PUT'])
def personalization_update(user_id):
    print("Request to update personalization for", user_id)

    data = flask.request.get_json()

    print("Data to update:", data)

    try:
        new_personalization = data.get('personalization')["personalizedPrompt"]

        cursor = make_connection(mysql)
        update_personalization(user_id, new_personalization, cursor)
        cursor.close()

        print("Personalization updated successfully")
        return flask.jsonify({'message': 'Personalization updated successfully'}), 200
    except Exception as e:
        cursor.close()

        print("Error updating personalization:", e)
        return flask.jsonify({'message': 'Something went wrong'}), 500

# Run the app
if __name__ == "__main__":
    with app.app_context():
        print("Initializing database...")

        try:
            init_database(mysql)
        except Exception as e:
            print("Error occurred while initializing database", e)
            exit(1)

    print("Starting server...")
    app.run(debug=True, host="0.0.0.0", port=5000)