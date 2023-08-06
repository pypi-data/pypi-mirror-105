from indice_pollution.models import db

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_zone = db.Column(db.String)
    code_zone = db.Column(db.String)
