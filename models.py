from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from config import db

# Association model
class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    __table_args__ = (
        UniqueConstraint('guest_id', 'episode_id', name='uq_guest_episode_once'),
    )

    @validates('rating')
    def validate_rating(self, key, value):
        if value is None:
            raise ValueError('rating required')
        try:
            ivalue = int(value)
        except Exception:
            raise ValueError('rating must be integer')
        if ivalue < 1 or ivalue > 5:
            raise ValueError('rating must be between 1 and 5')
        return ivalue

    def to_dict_for_episode(self):
        # For GET /episodes/<id>: include nested guest only
        return {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id,
            'guest': self.guest.to_dict_basic() if self.guest else None,
        }

    def to_dict_with_episode_and_guest(self):
        # For POST /appearances success payload
        return {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id,
            'episode': self.episode.to_dict_basic() if self.episode else None,
            'guest': self.guest.to_dict_basic() if self.guest else None,
        }

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False, unique=True)

    appearances = db.relationship(
        'Appearance', back_populates='episode', cascade='all, delete-orphan'
    )

    def to_dict_basic(self):
        return {
            'id': self.id,
            'date': self.date,
            'number': self.number,
        }

    def to_dict_detail_for_show(self):
        return {
            'id': self.id,
            'date': self.date,
            'number': self.number,
            'appearances': [ap.to_dict_for_episode() for ap in self.appearances]
        }

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    appearances = db.relationship(
        'Appearance', back_populates='guest', cascade='all, delete-orphan'
    )

    def to_dict_basic(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation,
        }