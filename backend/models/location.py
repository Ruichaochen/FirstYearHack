from database import db


class Location(db.Model):
    """Model for a cultural location in London."""

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # film, music, literature, tv, theatre
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(300), nullable=True)
    media_url = db.Column(db.String(500), nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        """Convert the location to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "media_url": self.media_url,
            "year": self.year,
        }
