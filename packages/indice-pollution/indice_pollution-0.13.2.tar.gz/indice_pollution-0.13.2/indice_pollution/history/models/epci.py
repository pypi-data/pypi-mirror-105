from indice_pollution.models import db
from sqlalchemy.orm import relation, relationship

class ECPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departement_id = db.Column(db.Integer, db.ForeignKey("indice_schema.departement.id"))
    departement = relationship("indice_pollution.history.models.departement.Departement")
    zone_id = db.Column(db.Integer)
    zone = relationship("indice_pollution.history.models.zone.Zone")