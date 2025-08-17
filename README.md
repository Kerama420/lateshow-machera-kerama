# lateshow-machera-kerama
# Late Show API (Flask)

Rubric-aligned solution for the Phase 4 Code Challenge. Implements:

- Models: `Episode`, `Guest`, `Appearance`
- Relationships: many-to-many `Episode ↔ Guest` through `Appearance`
- Cascade deletes on `Episode.appearances` and `Guest.appearances`
- Validation: `Appearance.rating` in **[1..5]** (inclusive)
- Routes: `GET /episodes`, `GET /episodes/<id>`, `DELETE /episodes/<id>`, `GET /guests`, `POST /appearances`
- Response structures exactly as required

## Quickstart

```bash
# 1) Create & activate a virtualenv (example with pipenv or venv)
pip install pipenv && pipenv install -r requirements.txt && pipenv shell
# or
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 2) Set Flask app and init DB
export FLASK_APP=app.py
flask db init   # only once, creates migrations folder
flask db migrate -m "init"
flask db upgrade

# 3) Seed data
python seed.py

# 4) Run
flask run -p 5555