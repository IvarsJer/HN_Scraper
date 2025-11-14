import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from models import Article, db


class HNScraper:
    def __init__(self, base_url: str = 'https://news.ycombinator.com/'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_articles(self) -> List[Dict]:
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            article_rows = soup.find_all('tr', class_='athing')

            for row in article_rows:
                try:
                    article_data = self._parse_article_row(row, soup)
                    if article_data:
                        articles.append(article_data)
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue

            return articles

        except requests.RequestException as e:
            print(f"Error fetching Hacker News: {e}")
            return []

    def _parse_article_row(self, row, soup) -> Optional[Dict]:
        hn_id = row.get('id')
        if not hn_id:
            return None

        title_span = row.find('span', class_='titleline')
        if not title_span:
            return None

        title_link = title_span.find('a')
        if not title_link:
            return None

        title = title_link.get_text(strip=True)
        link = title_link.get('href', '')

        if link and not link.startswith('http'):
            link = f"{self.base_url}{link}"

        meta_row = row.find_next_sibling('tr')
        points = 0
        date_created = None

        if meta_row:
            score_span = meta_row.find('span', class_='score')
            if score_span:
                points_text = score_span.get_text(strip=True)
                points_match = re.search(r'(\d+)', points_text)
                if points_match:
                    points = int(points_match.group(1))

            age_span = meta_row.find('span', class_='age')
            if age_span:
                date_created = self._parse_date(age_span.get('title', ''))

        return {
            'hn_id': hn_id,
            'title': title,
            'link': link,
            'points': points,
            'date_created': date_created
        }

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str:
            return None

        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            return None

    def save_articles(self, articles: List[Dict]) -> tuple:
        saved = 0
        updated = 0

        for article_data in articles:
            try:
                existing = Article.query.filter_by(hn_id=article_data['hn_id']).first()

                if existing:
                    existing.points = article_data['points']
                    existing.date_updated = datetime.utcnow()
                    updated += 1
                else:
                    article = Article(
                        hn_id=article_data['hn_id'],
                        title=article_data['title'],
                        link=article_data['link'],
                        points=article_data['points'],
                        date_created=article_data['date_created']
                    )
                    db.session.add(article)
                    saved += 1

                db.session.commit()

            except Exception as e:
                print(f"Error saving article {article_data.get('hn_id')}: {e}")
                db.session.rollback()
                continue

        return saved, updated

    def update_points(self) -> int:
        articles = self.scrape_articles()
        hn_id_to_points = {a['hn_id']: a['points'] for a in articles}

        updated = 0
        for hn_id, new_points in hn_id_to_points.items():
            try:
                article = Article.query.filter_by(hn_id=hn_id).first()
                if article and article.points != new_points:
                    article.points = new_points
                    article.date_updated = datetime.utcnow()
                    db.session.commit()
                    updated += 1
            except Exception as e:
                print(f"Error updating article {hn_id}: {e}")
                db.session.rollback()
                continue

        return updated