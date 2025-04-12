from flask import Blueprint, request, jsonify
from api.extensions import mysql
from llm.tiamat import Tiamat
from llm.personas import Persona
from api.util.tiamat_db_functions import make_connection, get_personalization, get_persona

prompt_bp = Blueprint('prompt', __name__)
chat = Tiamat()

@prompt_bp.route('/prompt', methods=['POST'])
def prompt_tiamat():
    data = request.get_json()
    user_id = data.get('id')
    message = data.get('message')
    code = data.get('code') or ''
    history = data.get('history') or []
    personalize = data.get('personalize') or False
    persona_name = data.get('persona') or None

    if not message or not user_id:
        return jsonify({'message': 'Some required data is missing'}), 400

    cursor = make_connection(mysql)
    personalization = get_personalization(user_id, cursor) if personalize else ""

    persona = Persona()
    if persona_name:
        persona_from_db = get_persona(persona_name, cursor)
        if not persona_from_db:
            return jsonify({'message': 'Persona not found'}), 404
        persona = Persona(
            name=persona_from_db[1],
            description=persona_from_db[2],
            prompt=persona_from_db[3]
        )

    cursor.close()

    response = chat(
        message, 
        code=code, 
        history=history, 
        personalization=personalization,
        persona=persona
    )

    return jsonify({'response': response.answer})