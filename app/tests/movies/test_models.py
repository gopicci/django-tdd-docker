import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_movie_model():
    movie = Movie(title="Ciao bella", genre="comedy", year="1952")
    movie.save()
    assert movie.title == "Ciao bella"
    assert movie.genre == "comedy"
    assert movie.year == "1952"
    assert movie.created_date
    assert movie.updated_date
    assert str(movie) == movie.title
