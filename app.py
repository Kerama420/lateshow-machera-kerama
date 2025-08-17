from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from config import db
from models import Episode, Guest, Appearance

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app)
db.init_app(app)
Migrate(app, db)

# -----------------------------
# Helpers for consistent errors
# -----------------------------

def error_response(message, status=400):
    return jsonify({"errors": [message]}) if status == 400 else (jsonify({"error": message}), status)

# -----------------------------
# Routes
# -----------------------------

@app.get('/')
def index():
    return jsonify({"message": "Late Show API running. See /episodes, /guests, /appearances (POST)"})

# a. GET /episodes
@app.get('/episodes')
def get_episodes():
    episodes = Episode.query.order_by(Episode.number.asc()).all()
    return jsonify([e.to_dict_basic() for e in episodes])

# b. GET /episodes/<id>
@app.get('/episodes/<int:id>')
def get_episode(id):
    ep = Episode.query.get(id)
    if not ep:
        return error_response("Episode not found", status=404)
    return jsonify(ep.to_dict_detail_for_show())

# (included in Postman) DELETE /episodes/<id>
@app.delete('/episodes/<int:id>')
def delete_episode(id):
    ep = Episode.query.get(id)
    if not ep:
        return error_response("Episode not found", status=404)
    db.session.delete(ep)
    db.session.commit()
    return ('', 204)

# c. GET /guests
@app.get('/guests')
def get_guests():
    guests = Guest.query.order_by(Guest.id.asc()).all()
    return jsonify([g.to_dict_basic() for g in guests])

# d. POST /appearances
@app.post('/appearances')
def create_appearance():
    data = request.get_json() or {}
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    # Ensure referenced rows exist
    episode = Episode.query.get(episode_id) if episode_id is not None else None
    guest = Guest.query.get(guest_id) if guest_id is not None else None

    if not episode or not guest:
        return error_response("validation errors", status=400)

    try:
        ap = Appearance(rating=rating, episode=episode, guest=guest)
        db.session.add(ap)
        db.session.commit()
    except (ValueError, IntegrityError):
        db.session.rollback()
        return error_response("validation errors", status=400)

    # Response matches spec (includes nested episode & guest)
    return jsonify(ap.to_dict_with_episode_and_guest()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)