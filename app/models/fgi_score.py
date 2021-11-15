from .. import db
from datetime import datetime, date
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

class Fgi_score(db.Model):
    __tablename__ = 'Fgi_Scores'
    id = db.Column('id', db.Integer, primary_key=True)
    score_time = db.Column('score_time', db.DateTime)
    fgi_value = db.Column('fgi_value', db.Integer)
    fgi_text = db.Column('fgi_text', db.String)
    updated_cnn = db.Column('updated_cnn', db.String)

    def add_score(self):
        db.session.add(self)
        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

