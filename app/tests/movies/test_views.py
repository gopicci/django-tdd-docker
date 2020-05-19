import pytest
from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Ciuruma", "genre": "horror", "year": "2018", },
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "Ciuruma"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post("/api/movies/", {}, content_type="application/json")
    assert resp.status_code == 400

    movies == Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Ciuruma", "genre": "horror", },
        content_type="application/json",
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="Ciuruma", genre="horror", year="2018")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Ciuruma"


def test_get_single_movie_incorrect_id(client):
    resp = client.get(f"/api/movies/foo/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="Ciuruma", genre="horror", year="2018")
    movie_two = add_movie("Barbapapa", "fantasy", "1750")
    resp = client.get(f"/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="Ciuruma", genre="horror", year="2018")

    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Ciuruma"

    resp_two = client.delete(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 204

    resp_three = client.get(f"/api/movies/")
    assert resp.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    resp = client.delete(f"/api/movie/99/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    movie = add_movie(title="Ciuruma", genre="horror", year="2018")

    resp = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "Ciuruma", "genre": "horror", "year": "2017"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.data["title"] == "Ciuruma"
    assert resp.data["year"] == "2017"

    resp_two = client.get(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 200
    assert resp_two.data["title"] == "Ciuruma"
    assert resp_two.data["year"] == "2017"


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    resp = client.put(f"/api/movies/99/")
    assert resp.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_movie, payload, status_code",
    [
        ["add_movie", {}, 400],
        ["add_movie", {"title": "Ciuruma", "genre": "horror"}, 400],
    ],
    indirect=["add_movie"],
)
def test_update_movie_invalid_json(client, add_movie, payload, status_code):
    movie = add_movie(title="Ciuruma", genre="horror", year="2018")
    resp = client.put(
        f"/api/movies/{movie.id}/", payload, content_type="application/json"
    )
    assert resp.status_code == status_code
