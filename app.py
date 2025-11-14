from flask import Flask, jsonify, request
from flask_cors import CORS
from config import config
from models import db, Article
from scraper import HNScraper
import click


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app)

    register_commands(app)

    # API Routes
    @app.route('/api/articles', methods=['GET'])
    def get_articles():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            sort_by = request.args.get('sort_by', 'date_scraped')
            order = request.args.get('order', 'desc')

            query = Article.query

            if hasattr(Article, sort_by):
                column = getattr(Article, sort_by)
                if order == 'desc':
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())

            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            return jsonify({
                'articles': [article.to_dict() for article in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/articles/<int:article_id>', methods=['GET'])
    def get_article(article_id):
        article = Article.query.get_or_404(article_id)
        return jsonify(article.to_dict())

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'})

    return app


def register_commands(app):

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        click.echo('Database initialized successfully!')

    @app.cli.command('scrape')
    @click.option('--update', is_flag=True, help='Update points for existing articles')
    def scrape_command(update):
        scraper = HNScraper(app.config['HN_URL'])

        if update:
            click.echo('Updating points for existing articles...')
            updated = scraper.update_points()
            click.echo(f'Updated {updated} articles')
        else:
            click.echo('Scraping articles from Hacker News...')
            articles = scraper.scrape_articles()
            click.echo(f'Found {len(articles)} articles')

            saved, updated = scraper.save_articles(articles)
            click.echo(f'Saved {saved} new articles, updated {updated} existing articles')

    @app.cli.command('drop-db')
    def drop_db():
        if click.confirm('Are you sure you want to drop all tables?'):
            db.drop_all()
            click.echo('Database tables dropped!')


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)