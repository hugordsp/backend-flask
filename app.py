from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True,
    error_messages={
        "required": "Foi João Rock",  # You can change
        "null": "Field may not be null.",  # You can change
        "validator_failed": "Invalid value.",  # You can change
        "invalid": "It's not a valid email."  # You can change
    })


# Simulando um banco de dados de usuários (usuário:senha)
users = {
    "usuario1": "senha1",
    "usuario2": "senha2",
}

# Rota de login


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    schema = LoginSchema()

    try:
        # Validate request body against schema data types
        result = schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400

    username = result["username"]
    password = result["password"]

    if username in users and users[username] == password:
        return jsonify({"message": "Login bem-sucedido"})
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401


if __name__ == "__main__":
    app.run(debug=True)
