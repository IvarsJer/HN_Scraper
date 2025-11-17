import pytest
from app import create_app
from models import db, Article


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def sample_articles(app):
    articles = [
        Article(
            hn_id='12345',
            title='Test Article 1',
            link='https://example.com/1',
            points=100
        ),
        Article(
            hn_id='12346',
            title='Test Article 2',
            link='https://example.com/2',
            points=200
        ),
        Article(
            hn_id='12347',
            title='Test Article 3',
            link='https://example.com/3',
            points=50
        )
    ]

    with app.app_context():
        for article in articles:
            db.session.add(article)

        db.session.commit()

        # Refresh the articles to reload their data
        for article in articles:
            db.session.refresh(article)

        yield articles

        # Cleanup after test
        db.session.query(Article).delete()
        db.session.commit()