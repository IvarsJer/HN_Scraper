.PHONY: help build up down logs scrape test clean restart

help:
	@echo "Hacker News Scraper - Available commands:"
	@echo "  make build      - Build Docker containers"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs"
	@echo "  make scrape     - Run the scraper"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Remove containers and volumes"
	@echo "  make restart    - Restart all services"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

scrape:
	docker-compose exec backend flask scrape

test:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	rm -rf htmlcov .coverage .pytest_cache

restart:
	docker-compose restart