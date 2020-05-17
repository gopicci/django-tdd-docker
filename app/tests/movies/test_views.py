import json
import pytest
from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/api/movies/',
        {
            'title': 'Ciuruma',
            'genre': 'horror',
            'year': '2018',
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['title'] == 'Ciuruma'

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/api/movies/',
        {},
        content_type='application/json'
    )
    assert resp.status_code == 400

    movies == Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "Ciuruma",
            "genre": "horror",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title='Ciuruma', genre='horror', year='2018')
    resp = client.get(f'/api/movies/{movie.id}/')
    assert resp.status_code == 200
    assert resp.data['title'] == 'Ciuruma'


def test_get_single_movie_incorrect_id(client):
    resp = client.get(f'/api/movies/foo/')
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title='Ciuruma', genre='horror', year='2018')
    movie_two = add_movie('Barbapapa', 'fantasy', '1750')
    resp = client.get(f'/api/movies/')
    assert resp.status_code == 200
    assert resp.data[0]['title'] == movie_one.title
    assert resp.data[1]['title'] == movie_two.title
