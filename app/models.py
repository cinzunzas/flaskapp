from .app import db

class favorite_colors(db.Model):
    __tablename__ = 'favorite_colors'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20))
    color = db.Column('color', db.String(10))
