import pytest
from server.app import app, db
from server.models import Customer, Item, Review

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Create all tables
    with app.app_context():
        db.create_all()
    
    yield app.test_client()
    
    # Clean up after tests
    with app.app_context():
        db.drop_all()

def test_create_customer(client):
    with app.app_context():
        customer = Customer(name='Test Customer')
        db.session.add(customer)
        db.session.commit()
        assert customer.id is not None
        assert customer.name == 'Test Customer'

def test_create_item(client):
    with app.app_context():
        item = Item(name='Test Item', price=19.99)
        db.session.add(item)
        db.session.commit()
        assert item.id is not None
        assert item.name == 'Test Item'
        assert item.price == 19.99

def test_create_review(client):
    with app.app_context():
        customer = Customer(name='Test Customer')
        item = Item(name='Test Item', price=19.99)
        db.session.add(customer)
        db.session.add(item)
        db.session.commit()

        review = Review(comment='Great product!', customer=customer, item=item)
        db.session.add(review)
        db.session.commit()
        assert review.id is not None
        assert review.comment == 'Great product!'
        assert review.customer_id == customer.id
        assert review.item_id == item.id