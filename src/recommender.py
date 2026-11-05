"""Content-based music recommendation logic for the CodePath simulation."""

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Song:
    """Store the catalog attributes of one song."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Store a user's preferred genre, mood, energy, and acoustic sound."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


DEFAULT_WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0}
EXPERIMENT_WEIGHTS = {"genre": 1.0, "mood": 1.0, "energy": 2.0}


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric fields to numbers."""
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with Path(csv_path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=2):
            try:
                row["id"] = int(row["id"])
                for field in numeric_fields:
                    row[field] = float(row[field])
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Invalid numeric data in CSV row {row_number}: {exc}") from exc
            for field in ("energy", "valence", "danceability", "acousticness"):
                if not 0 <= row[field] <= 1:
                    raise ValueError(f"{field} must be between 0 and 1 (row {row_number})")
            if row["tempo_bpm"] <= 0:
                raise ValueError(f"tempo_bpm must be positive (row {row_number})")
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, List[str]]:
    """Calculate one song's weighted relevance and human-readable reasons."""
    weights = DEFAULT_WEIGHTS if weights is None else weights
    score = 0.0
    reasons: List[str] = []

    genre = str(user_prefs.get("genre", "")).strip().casefold()
    mood = str(user_prefs.get("mood", "")).strip().casefold()
    if genre and genre == str(song["genre"]).strip().casefold():
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")
    if mood and mood == str(song["mood"]).strip().casefold():
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    target_energy = float(user_prefs["energy"])
    if not 0 <= target_energy <= 1:
        raise ValueError("User energy preference must be between 0 and 1")
    energy_similarity = 1 - abs(float(song["energy"]) - target_energy)
    energy_points = weights["energy"] * energy_similarity
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    # Only OOP profiles explicitly provide an acoustic preference; the basic CLI
    # uses the three-feature recipe, whose maximum score is exactly 4.0.
    if "likes_acoustic" in user_prefs:
        acousticness = float(song["acousticness"])
        acoustic_points = 0.5 * (acousticness if user_prefs["likes_acoustic"] else 1 - acousticness)
        score += acoustic_points
        reasons.append(f"acoustic preference (+{acoustic_points:.2f})")

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the top k with explanations."""
    if k <= 0:
        return []
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, ", ".join(reasons)))
    # sorted() leaves the original catalog unchanged; stable ties use song title.
    return sorted(scored, key=lambda result: (-result[1], result[0]["title"].casefold()))[:k]


class Recommender:
    """Provide an object-oriented adapter for the same recommendation logic."""

    def __init__(self, songs: List[Song]):
        """Store the song catalog for this recommender."""
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Translate a UserProfile to the functional scoring format."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the highest-ranked Song objects for a user's profile."""
        scores = recommend_songs(self._prefs(user), [asdict(song) for song in self.songs], k)
        id_to_song = {song.id: song for song in self.songs}
        return [id_to_song[item["id"]] for item, _, _ in scores]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a particular Song object's score in readable language."""
        score, reasons = score_song(self._prefs(user), asdict(song))
        return f"{song.title} scored {score:.2f}: " + ", ".join(reasons)
