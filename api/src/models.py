from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    public_id = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "public_id": self.public_id
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()