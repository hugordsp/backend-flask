from flask import Flask, jsonify, request
from marshmallow import Schema, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://app_user:123456@localhost/backend_A3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class UserSchema(Schema):
    class Meta:
        fields = ("id", "username", "password")

# List all USERS


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result)

# List USERS by ID


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return jsonify(result)
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

# Create USER


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Usuário com esse nome de usuário já existe"}), 400

    password = data.get("password")
    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso"})

# update USER


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get("username")

        if User.query.filter(User.id != user_id, User.username == username).first():
            return jsonify({"message": "Já existe um usuário com esse nome."}), 400

        schema = UserSchema()

        try:
            updated_user_data = schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Copie os dados atualizados para o objeto do usuário existente
        user.username = updated_user_data["username"]
        user.password = updated_user_data["password"]

        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso"})
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404


# Delete USER


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"})
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
