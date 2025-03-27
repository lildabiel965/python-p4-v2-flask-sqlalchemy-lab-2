# testing/association_proxy_test.py
import pytest
from app import app, db
from server.models import Customer, Item, Review

@pytest.fixture(autouse=True)
def setup_db():
    """Setup database for testing"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            # Create test data with required fields
            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=10.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Create review to establish relationship
            r = Review(comment='great!', customer=c, item=i)
            db.session.add