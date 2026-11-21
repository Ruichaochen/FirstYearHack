from database import db


class LocationProduction(db.Model):
    """Association object for the many-to-many relationship between locations and productions.

    Stores the source of each production link (e.g., "top_modelled", "top_productions",
    "verified_productions", "top_verified") so we know which CSV field it came from.
    """

    __tablename__ = "location_productions"

    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), primary_key=True)
    production_source = db.Column(db.String(50), nullable=True)  # "top_modelled", "top_productions", etc.

    location = db.relationship("Location", back_populates="location_productions_entries")
    production = db.relationship("Production", back_populates="location_productions_entries")


class Production(db.Model):
    """Model for a production (film, TV show, etc.) associated with one or more locations."""

    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False, unique=True)

    location_productions_entries = db.relationship(
        "LocationProduction", back_populates="production", cascade="all, delete-orphan"
    )

    def to_dict(self, source=None):
        d = {
            "id": self.id,
            "name": self.name,
        }
        if source is not None:
            d["production_source"] = source
        return d


class Location(db.Model):
    """Model for a cultural location in London."""

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.String(50), nullable=True, unique=True)  # Wikidata QID
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # film, music, literature, tv, theatre
    category_label = db.Column(db.String(100), nullable=True)  # Human-readable category
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(100), nullable=True)
    iso = db.Column(db.String(10), nullable=True)  # ISO country code
    address = db.Column(db.String(300), nullable=True)
    resolution = db.Column(db.String(50), nullable=True)
    fame_rank = db.Column(db.Integer, nullable=True)
    fame_tier = db.Column(db.String(20), nullable=True)
    wiki_productions = db.Column(db.Integer, nullable=True)
    modelled_for = db.Column(db.Integer, nullable=True)
    wikipedia = db.Column(db.String(500), nullable=True)
    wikidata = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(500), nullable=True)
    image_page = db.Column(db.String(500), nullable=True)
    image_by = db.Column(db.String(200), nullable=True)
    image_licence = db.Column(db.String(200), nullable=True)
    image_licence_url = db.Column(db.String(500), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    media_url = db.Column(db.String(500), nullable=True)  # Legacy field, maps to image
    year = db.Column(db.Integer, nullable=True)

    # Relationship to the association object so we can access production_source per link
    location_productions_entries = db.relationship(
        "LocationProduction", back_populates="location", lazy="select",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Convert the location to a dictionary for JSON serialization."""
        # Build productions list with source info from the association table
        productions = []
        for lp in self.location_productions_entries:
            productions.append(lp.production.to_dict(source=lp.production_source))

        return {
            "id": self.id,
            "qid": self.qid,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "category_label": self.category_label,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "country": self.country,
            "iso": self.iso,
            "resolution": self.resolution,
            "fame_rank": self.fame_rank,
            "fame_tier": self.fame_tier,
            "wiki_productions": self.wiki_productions,
            "modelled_for": self.modelled_for,
            "wikipedia": self.wikipedia,
            "wikidata": self.wikidata,
            "image": self.image,
            "image_page": self.image_page,
            "image_by": self.image_by,
            "image_licence": self.image_licence,
            "image_licence_url": self.image_licence_url,
            "url": self.url,
            "media_url": self.media_url,
            "year": self.year,
            "productions_list": productions,
        }
