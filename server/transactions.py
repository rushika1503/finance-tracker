from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, User, db

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api')

@transactions_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": t.id,
            "label": t.label,
            "amount": t.amount,
            "type": t.type,
            "date": t.date
        } for t in transactions
    ])

@transactions_bp.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_txn = Transaction(
        user_id=user_id,
        label=data["label"],
        amount=data["amount"],
        type=data["type"],
        date=data["date"]
    )

    db.session.add(new_txn)
    db.session.commit()
    return jsonify({"message": "Transaction added"}), 201


@transactions_bp.route('/transactions/<int:txn_id>', methods=['PUT'])
@jwt_required()
def update_transaction(txn_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    print("Incoming PUT body:", data)

    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 422

    txn = Transaction.query.filter_by(id=txn_id, user_id=user_id).first()
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404

    txn.label = data.get("label", txn.label)
    txn.amount = data.get("amount", txn.amount)
    txn.type = data.get("type", txn.type)
    txn.date = data.get("date", txn.date)

    db.session.commit()
    return jsonify({"message": "Transaction updated"}), 200


@transactions_bp.route('/transactions/<int:txn_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(txn_id):
    user_id = get_jwt_identity()
    txn = Transaction.query.filter_by(id=txn_id, user_id=user_id).first()

    if not txn:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(txn)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"}), 200








# @transactions_bp.route('/transactions', methods=['POST'])
# @jwt_required()
# def add_transaction():
#     user_id = get_jwt_identity()
#     data = request.get_json()

#     if isinstance(data, list):  # Handle bulk insert
#         for txn in data:
#             new_txn = Transaction(
#                 user_id=user_id,
#                 label=txn["label"],
#                 amount=txn["amount"],
#                 type=txn["type"],
#                 date=txn["date"]
#             )
#             db.session.add(new_txn)
#     else:
#         new_txn = Transaction(
#             user_id=user_id,
#             label=data["label"],
#             amount=data["amount"],
#             type=data["type"],
#             date=data["date"]
#         )
#         db.session.add(new_txn)

#     db.session.commit()
#     return jsonify({"message": "Transaction(s) added successfully"})

