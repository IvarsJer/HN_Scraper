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

### Using Docker Compose (Standard)

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

### Using Makefile (Linux/Unix)

For Linux users, a Makefile is provided for easier command execution:

1. Copy environment file:
```bash
cp .env.example .env
```

2. View available commands:
```bash
make help
```

3. Build and start services:
```bash
make build
make up
```

4. Run the scraper:
```bash
make scrape
```

5. Open http://localhost:3000

#### Available Makefile Commands
```bash
make build      # Build Docker containers
make up         # Start all services in detached mode
make down       # Stop all services
make logs       # View live logs from all services
make scrape     # Run the Hacker News scraper
make test       # Run unit tests
make clean      # Remove containers, volumes, and test artifacts
make restart    # Restart all services
```

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

### Flask Commands (Manual Setup)
```bash
flask scrape              # Scrape articles
flask scrape --update     # Update points
flask init-db             # Initialize database
pytest                    # Run tests
```

### Docker Commands (Standard)
```bash
docker-compose up --build              # Build and start services
docker-compose down                    # Stop services
docker-compose exec backend flask scrape    # Run scraper
docker-compose logs -f                 # View logs
```

## Tech Stack

* Backend: Flask, SQLAlchemy, BeautifulSoup
* Frontend: React, DataTables
* Database: PostgreSQL
* Docker: docker-compose