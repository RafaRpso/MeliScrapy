# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gross_value = db.Column(db.Numeric(10, 2), nullable=False)
    percent = db.Column(db.Integer, nullable=False)


class Cupom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False)
    link = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    fk_cupom = db.Column(db.Integer, db.ForeignKey('cupom.id'))
    fk_promotion = db.Column(db.Integer, db.ForeignKey('promotion.id'))

    cupom = db.relationship('Cupom', backref=db.backref('products', lazy=True))
    promotion = db.relationship(
        'Promotion', backref=db.backref('products', lazy=True))

    __table_args__ = (db.UniqueConstraint(
        'title', 'price', 'category_name', 'image', 'link', name='unique_product'),)
