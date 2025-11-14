# Hacker News Scraper

Web scraper that collects articles from Hacker News and displays them in a table. Built with Flask, PostgreSQL, and React.

## Features

- Scrapes article title, link, points, and date from Hacker News
- Stores data in PostgreSQL database
- Updates article points
- Web interface with DataTables (10 items per page)
- Docker support
- Unit tests included

## Setup with Docker

1. Copy environment file:
```bash
cp .env.example .env
```

2. Start everything:
```bash
docker-compose up --build
```

3. Run the scraper:
```bash
docker-compose exec backend flask scrape
```

4. Open http://localhost:3000

## Manual Setup (without Docker)

### Backend

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create PostgreSQL database:
```bash
createdb hn_scraper
```

3. Setup environment:
```bash
cp .env.example .env
```
Edit `.env` with your database credentials.

4. Initialize database:
```bash
export FLASK_APP=app.py
flask init-db
```

5. Run scraper:
```bash
flask scrape
```

6. Start server:
```bash
python app.py
```

### Frontend

1. Install and start:
```bash
cd frontend
npm install
npm start
```

2. Open http://localhost:3000

## Commands
```bash
flask scrape              # Scrape articles
flask scrape --update     # Update points
flask init-db             # Initialize database
pytest                    # Run tests
```

## Tech Stack

* Backend: Flask, SQLAlchemy, BeautifulSoup
* Frontend: React, DataTables
* Database: PostgreSQL
* Docker: docker-compose