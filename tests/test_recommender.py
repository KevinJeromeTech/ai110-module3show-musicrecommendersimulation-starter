from pathlib import Path

import pytest

from src.recommender import (
    EXPERIMENT_WEIGHTS,
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)


def make_small_recommender() -> Recommender:
    songs = [
        Song(1, "Test Pop Track", "Test Artist", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
        Song(2, "Chill Lofi Loop", "Test Artist", "lofi", "chill", 0.4, 80, 0.6, 0.5, 0.9),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile("pop", "happy", 0.8, False)
    results = make_small_recommender().recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile("pop", "happy", 0.8, False)
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre match" in explanation


def test_load_songs_casts_numbers():
    songs = load_songs(str(Path(__file__).resolve().parents[1] / "data" / "songs.csv"))
    assert len(songs) == 18
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)


def test_exact_match_has_full_basic_score_and_reasons():
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, song)
    assert score == 4.0
    assert len(reasons) == 3


def test_energy_similarity_rewards_closer_energy():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    close = {"genre": "rock", "mood": "sad", "energy": 0.75}
    distant = {"genre": "rock", "mood": "sad", "energy": 0.15}
    assert score_song(prefs, close)[0] > score_song(prefs, distant)[0]


def test_recommend_top_k_does_not_modify_catalog():
    songs = [
        {"title": "Low", "genre": "rock", "mood": "sad", "energy": 0.1},
        {"title": "High", "genre": "pop", "mood": "happy", "energy": 0.8},
    ]
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    result = recommend_songs(prefs, songs, k=1)
    assert result[0][0]["title"] == "High"
    assert len(result) == 1
    assert songs[0]["title"] == "Low"
    assert recommend_songs(prefs, songs, k=0) == []


def test_experiment_changes_point_weights():
    song = {"genre": "pop", "mood": "sad", "energy": 0.8}
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    baseline, _ = score_song(prefs, song)
    alternative, _ = score_song(prefs, song, EXPERIMENT_WEIGHTS)
    assert baseline == alternative == 3.0
    assert score_song(prefs, {"genre": "rock", "mood": "sad", "energy": 0.8}, EXPERIMENT_WEIGHTS)[0] == 2.0


def test_invalid_energy_rejected():
    with pytest.raises(ValueError):
        score_song({"genre": "pop", "mood": "happy", "energy": 5}, {"genre": "pop", "mood": "happy", "energy": 0.8})
