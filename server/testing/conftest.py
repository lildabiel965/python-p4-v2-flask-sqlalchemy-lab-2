#!/usr/bin/env python3
import pytest
from app import app, db
from server.models import Customer, Item, Review

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    """Setup database for all tests"""
    # Configure test database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # Create all tables
    with app.app_context():
        db.create_all()
    
    yield  # This is where testing happens
    
    # Clean up after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()
        
def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))