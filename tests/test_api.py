import json


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_get_articles_empty(client):
    response = client.get('/api/articles')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['total'] == 0
    assert data['articles'] == []


def test_get_articles(client, sample_articles):
    response = client.get('/api/articles?page=1&per_page=2')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['total'] == 3
    assert len(data['articles']) == 2
    assert data['per_page'] == 2


def test_get_single_article(client, sample_articles):
    article_id = sample_articles[0].id

    response = client.get(f'/api/articles/{article_id}')
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == article_id


def test_get_nonexistent_article(client):
    # Getting an article that doesn't exist
    response = client.get('/api/articles/99999')
    assert response.status_code == 404


def test_articles_sorting(client, sample_articles):
    # Sort by points descending
    response = client.get('/api/articles?sort_by=points&order=desc')
    assert response.status_code == 200

    data = json.loads(response.data)
    articles = data['articles']

    # Should be sorted by points (200, 100, 50)
    assert articles[0]['points'] >= articles[1]['points']
    assert articles[1]['points'] >= articles[2]['points']


def test_articles_pagination(client, sample_articles):
    # Get page 1 with 2 items
    response = client.get('/api/articles?page=1&per_page=2')
    data = json.loads(response.data)

    assert data['current_page'] == 1
    assert data['per_page'] == 2
    assert len(data['articles']) == 2
    assert data['pages'] == 2

    # Get page 2
    response = client.get('/api/articles?page=2&per_page=2')
    data = json.loads(response.data)

    assert data['current_page'] == 2
    assert len(data['articles']) == 1