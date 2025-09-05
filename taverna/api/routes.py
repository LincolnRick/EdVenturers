from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from taverna.models import Usuario

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/users/search')
def users_search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify({"results": []})
    results = (
        Usuario.query
        .filter(or_(Usuario.username.ilike(f"%{q}%"), Usuario.email.ilike(f"%{q}%")))
        .order_by(Usuario.username.asc())
        .limit(10)
        .all()
    )
    return jsonify({"results": [{"id": u.id, "name": u.username, "email": u.email} for u in results]})
