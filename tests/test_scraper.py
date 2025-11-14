from unittest.mock import Mock, patch
from scraper import HNScraper
from models import Article, db


def test_scraper_initialization():
    scraper = HNScraper('https://news.ycombinator.com/')
    assert scraper.base_url == 'https://news.ycombinator.com/'
    assert scraper.session is not None


def test_parse_date():
    scraper = HNScraper()

    date_str = '2024-01-15T10:30:00'
    parsed = scraper._parse_date(date_str)
    assert parsed is not None

    assert scraper._parse_date('') is None


def test_save_articles_new(app):
    with app.app_context():
        scraper = HNScraper()

        articles_data = [
            {
                'hn_id': 'test1',
                'title': 'Test Title 1',
                'link': 'https://example.com/1',
                'points': 100,
                'date_created': None
            },
            {
                'hn_id': 'test2',
                'title': 'Test Title 2',
                'link': 'https://example.com/2',
                'points': 200,
                'date_created': None
            }
        ]

        saved, updated = scraper.save_articles(articles_data)

        assert saved == 2
        assert updated == 0

        assert Article.query.count() == 2


def test_save_articles_update(app):
    with app.app_context():
        existing = Article(
            hn_id='test1',
            title='Test Title',
            link='https://example.com',
            points=50
        )
        db.session.add(existing)
        db.session.commit()

        scraper = HNScraper()

        articles_data = [
            {
                'hn_id': 'test1',
                'title': 'Test Title',
                'link': 'https://example.com',
                'points': 150,
                'date_created': None
            }
        ]

        saved, updated = scraper.save_articles(articles_data)

        assert saved == 0
        assert updated == 1

        article = Article.query.filter_by(hn_id='test1').first()
        assert article.points == 150


@patch('scraper.requests.Session.get')
def test_scrape_articles_error_handling(mock_get):
    mock_get.side_effect = Exception('Network error')

    scraper = HNScraper()
    articles = scraper.scrape_articles()

    assert articles == []