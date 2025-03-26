from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'customer': {  # Include customer as a dictionary with just the id and name
                'id': self.customer.id if self.customer else None,
                'name': self.customer.name if self.customer else None
            },
            'item': {  # Include item as a dictionary with just the id and name
                'id': self.item.id if self.item else None,
                'name': self.item.name if self.item else None,
                'price': self.item.price if self.item else None
        }
    }


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.id for review in self.reviews]  # Include only review IDs to avoid recursion
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.id for review in self.reviews]  # Include only review IDs to avoid recursion
        }
