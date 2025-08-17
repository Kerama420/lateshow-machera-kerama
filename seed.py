import csv
import os
from random import randint
from app import app, db, Episode, Guest, Appearance

CSV_PATH = os.path.join(os.path.dirname(__file__), 'lateshow.csv')

sample_episodes = [
    {"date": "1/11/99", "number": 1},
    {"date": "1/12/99", "number": 2},
    {"date": "1/13/99", "number": 3},
]

sample_guests = [
    {"name": "Michael J. Fox", "occupation": "actor"},
    {"name": "Sandra Bernhard", "occupation": "Comedian"},
    {"name": "Tracey Ullman", "occupation": "television actress"},
]

with app.app_context():
    print('🌱 Seeding…')
    db.drop_all()
    db.create_all()

    episodes = []
    guests = []

    # Load from CSV if present; else fall back to samples
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline='') as f:
            reader = csv.DictReader(f)
            # Expect columns: type (episode|guest), date, number, name, occupation
            for row in reader:
                if row.get('type') == 'episode':
                    e = Episode(date=row['date'], number=int(row['number']))
                    db.session.add(e)
                    episodes.append(e)
                elif row.get('type') == 'guest':
                    g = Guest(name=row['name'], occupation=row['occupation'])
                    db.session.add(g)
                    guests.append(g)
    else:
        episodes = [Episode(**e) for e in sample_episodes]
        guests = [Guest(**g) for g in sample_guests]
        db.session.add_all(episodes + guests)

    db.session.commit()

    # Create appearances with valid ratings
    if episodes and guests:
        a1 = Appearance(rating=4, episode=episodes[0], guest=guests[0])
        a2 = Appearance(rating=5, episode=episodes[1], guest=guests[2])
        a3 = Appearance(rating=3, episode=episodes[1], guest=guests[1])
        db.session.add_all([a1, a2, a3])
        db.session.commit()

    print('✅ Done.')