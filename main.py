import flask
import tiamat as tiamat

from flask_cors import CORS

# Create the Flask app
app = flask.Flask(__name__)
CORS(app)

conversations = {}

# Define a route
@app.route('/api/prompt', methods=['POST'])
def get_widget():
    # Extract the prompt from the request
    data = flask.request.get_json()
    conversation_id = data.get('id')
    message = data.get('message')

    if not message or not conversation_id:
        return flask.jsonify({'message': 'Some required data is missing'}), 400

    if conversation_id in conversations:
        chat = conversations[conversation_id]
        print(f"Existing conversation detected, id={conversation_id}")
        print(f"Last response: {chat.last_response}")
    else:
        chat = tiamat.Tiamat()
        conversations[conversation_id] = chat
        print(f"New conversation created, id={conversation_id}")

    print(f" User's message: {message}")

    response = chat(message)

    print(f"       Response: {response.answer}")
    print(f"Updated context: {chat.context}")

    # Return the widget as JSON
    return flask.jsonify({'response': response.answer})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
