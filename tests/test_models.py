from datetime import datetime
from models import Article, db


def test_article_creation(app):
    with app.app_context():
        article = Article(
            hn_id='123',
            title='Test Article',
            link='https://example.com',
            points=42
        )

        db.session.add(article)
        db.session.commit()

        retrieved = Article.query.filter_by(hn_id='123').first()
        assert retrieved is not None
        assert retrieved.title == 'Test Article'
        assert retrieved.points == 42


def test_article_to_dict(app):
    with app.app_context():
        article = Article(
            hn_id='456',
            title='Test Article',
            link='https://example.com',
            points=100
        )

        db.session.add(article)
        db.session.commit()

        article_dict = article.to_dict()

        assert article_dict['hn_id'] == '456'
        assert article_dict['title'] == 'Test Article'
        assert article_dict['points'] == 100
        assert 'id' in article_dict
        assert 'date_scraped' in article_dict


def test_article_unique_hn_id(app):
    with app.app_context():
        article1 = Article(
            hn_id='789',
            title='Article 1',
            link='https://example.com',
            points=10
        )

        article2 = Article(
            hn_id='789',
            title='Article 2',
            link='https://example.com',
            points=20
        )

        db.session.add(article1)
        db.session.commit()

        db.session.add(article2)

        try:
            db.session.commit()
            assert False, "Should have raised integrity error"
        except Exception:
            db.session.rollback()
            assert True


def test_article_update(app):
    with app.app_context():
        article = Article(
            hn_id='999',
            title='Test Article',
            link='https://example.com',
            points=50
        )

        db.session.add(article)
        db.session.commit()

        # Update points
        article.points = 150
        db.session.commit()

        retrieved = Article.query.filter_by(hn_id='999').first()
        assert retrieved.points == 150