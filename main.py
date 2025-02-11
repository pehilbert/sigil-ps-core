import flask
import tiamat as tiamat

from flask_cors import CORS

# Create the Flask app
app = flask.Flask(__name__)
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
